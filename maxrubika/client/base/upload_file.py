import base64
import os
import asyncio
import inspect
import aiohttp
import aiofiles
from typing import Callable, Optional, Union
import maxrubika
from ...data import Data
from .. import exceptions

class UploadFile:
    async def upload_file(
        self: "maxrubika.Client",
        file: Union[str, bytes, None] = None,
        base64_data: Optional[str] = None,
        mime: Optional[str] = None,
        file_name: Optional[str] = None,
        chunk: int = 1048576,
        callback: Optional[Callable[[int, int], Union[None, asyncio.Future]]] = None,
        *args, **kwargs
    ):
        """
        Upload a file to Rubika with chunked transfer and retry logic.

        Parameters:
            file (str, bytes, or None): File path, bytes, or URL to upload.
            base64_data (str, optional): Base64 encoded file data.
            mime (str, optional): MIME type of the file.
            file_name (str, optional): Name of the file.
            chunk (int, optional): Chunk size in bytes (default: 1MB).
            callback (callable, optional): Progress callback(total_size, uploaded_bytes).

        Returns:
            Metadata about the uploaded file.
        """
        if base64_data:
            try:
                file = base64.b64decode(base64_data)
            except Exception:
                raise exceptions.InvalidInput("Invalid base64 data.")

        if file is None:
            raise exceptions.InvalidInput("Either 'file' or 'base64_data' must be provided.")

        if isinstance(file, str):
            if file.startswith('http'):
                async with aiohttp.ClientSession() as session:
                    async with session.get(file) as resp:
                        file = await resp.read()
                file_name = file_name or file.split('/')[-1].split('?')[0]
                file_size = len(file)
            elif os.path.exists(file):
                file_name = file_name or os.path.basename(file)
                file_size = os.path.getsize(file)
            else:
                raise FileNotFoundError(
                    f"File not found: {file}\n"
                    "Please check if the file path is correct, "
                    "or provide the file as bytes or URL.")
        elif isinstance(file, bytes):
            if not file_name:
                raise exceptions.InvalidInput("'file_name' must be provided for byte or base64 uploads.")
            file_size = len(file)
        else:
            raise exceptions.InvalidInput("Expected a file path (str), raw bytes, or URL.")

        mime = mime or file_name.split(".")[-1] if file_name else "bin"
        max_retries = self.max_retries

        async def handle_callback(total: int, current: int):
            if not callable(callback):
                return
            try:
                if inspect.iscoroutinefunction(callback):
                    await callback(total, current)
                else:
                    callback(total, current)
            except exceptions.CancelledError:
                return None
            except Exception as e:
                self.logger.error(f"Callback error: {e}", exc_info=True)

        async def upload_chunk(data: bytes, part_number: int) -> dict:
            for attempt in range(max_retries):
                try:
                    async with self.connection.session.post(
                        url = upload_url,
                        headers = {
                            "auth": self.auth,
                            "file-id": file_id,
                            "total-part": str(total_parts),
                            "part-number": str(part_number),
                            "chunk-size": str(len(data)),
                            "access-hash-send": access_hash_send,
                        },
                        data=data,
                        proxy=self.proxy,
                    ) as response:
                        return await response.json()
                except Exception as e:
                    self.logger.warning(
                        f"Chunk {part_number} upload failed (attempt {attempt + 1}/{max_retries}): {e}"
                    )
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                    else:
                        raise

        result = await self.request_send_file(file_name, file_size, mime)
        file_id, dc_id, upload_url, access_hash_send = (
            result.id,
            result.dc_id,
            result.upload_url,
            result.access_hash_send,
        )
        total_parts = (file_size + chunk - 1) // chunk

        if total_parts == 0:
            return Data({
                "mime": mime,
                "size": 0,
                "dc_id": dc_id,
                "file_id": file_id,
                "file_name": file_name,
                "access_hash_rec": None
            })

        index = 0
        upload_result = None

        while index < total_parts:
            if isinstance(file, str) and os.path.exists(file):
                async with aiofiles.open(file, "rb") as f:
                    await f.seek(index * chunk)
                    data = await f.read(chunk)
            else:
                data = file[index * chunk : (index + 1) * chunk]

            upload_result = await upload_chunk(data, index + 1)

            if upload_result.get("status") == "ERROR_TRY_AGAIN":
                self.logger.warning("Server requested upload restart; reinitializing...")
                result = await self.request_send_file(file_name, file_size, mime)
                file_id, dc_id, upload_url, access_hash_send = (
                    result.id,
                    result.dc_id,
                    result.upload_url,
                    result.access_hash_send,
                )
                index = 0
                continue

            await handle_callback(file_size, min((index + 1) * chunk, file_size))
            index += 1

        if upload_result.get("status") == "OK" and upload_result.get("status_det") == "OK":
            return Data({
                "status": "OK",
                "mime": mime,
                "size": file_size,
                "dc_id": dc_id,
                "file_id": file_id,
                "file_name": file_name,
                "access_hash_rec": upload_result["data"]["access_hash_rec"],
            })

        error_type = upload_result.get("status_det") or "UnknownError"
        if hasattr(exceptions, error_type):
            raise getattr(exceptions, error_type)(upload_result)
        else:
            raise exceptions.InvalidInput(
                f"Upload failed: {upload_result}")