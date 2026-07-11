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
        file: Union[str, bytes],
        mime: Optional[str] = None,
        file_name: Optional[str] = None,
        chunk: int = 1048576,
        callback: Optional[Callable[[int, int], Union[None, asyncio.Future]]] = None,
        *args, **kwargs
    ):
        """
        Upload a file to Rubika with chunked transfer and retry logic.

        Parameters:
            file (str or bytes): File path or bytes to upload.
            mime (str, optional): MIME type of the file.
            file_name (str, optional): Name of the file.
            chunk (int, optional): Chunk size in bytes (default: 1MB).
            callback (callable, optional): Progress callback(total_size, uploaded_bytes).

        Returns:
            Metadata about the uploaded file.
        """
        if isinstance(file, str):
            if not os.path.exists(file):
                raise exceptions.InvalidInput("Unable to locate file at the given path.")
            file_name = file_name or os.path.basename(file)
            file_size = os.path.getsize(file)
        elif isinstance(file, bytes):
            if not file_name:
                raise exceptions.InvalidInput("'file_name' must be provided for byte uploads.")
            file_size = len(file)
        else:
            raise exceptions.InvalidInput("Expected a file path (str) or raw bytes.")

        mime = mime or file_name.split(".")[-1]
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
                self.logger.error(f"Callback error: {e}")

        async def upload_chunk(data: bytes, part_number: int) -> dict:
            for attempt in range(max_retries):
                try:
                    async with self.connection.session.post(
                        url=upload_url,
                        headers={
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
            if isinstance(file, str):
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
                "mime": mime,
                "size": file_size,
                "dc_id": dc_id,
                "file_id": file_id,
                "file_name": file_name,
                "access_hash_rec": upload_result["data"]["access_hash_rec"],
            })

        raise getattr(exceptions, upload_result.get("status_det"))(upload_result)