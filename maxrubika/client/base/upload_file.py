import asyncio
from typing import Callable, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UploadFile:
    async def upload_file(
        self: "maxrubika.Messenger",
        file: Union[str, bytes, None] = None,
        base64_data: Optional[str] = None,
        mime: Optional[str] = None,
        file_name: Optional[str] = None,
        chunk: int = 1048576,
        callback: Optional[Callable[[int, int], Optional["asyncio.Future"]]] = None
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
            Data or dict: Metadata about the uploaded file.
                - If `as_dict=True` on the client, returns a plain dict.
                - Otherwise, returns a Data object.
        """
        import os
        import base64
        import inspect
        import aiohttp
        import aiofiles
        from ...data import Data
        from .. import exceptions

        if base64_data and file is not None:
            raise exceptions.InvalidInput("Provide either 'file' or 'base64_data', not both.")

        if base64_data:
            try:
                file = base64.b64decode(base64_data)
            except Exception:
                raise exceptions.InvalidInput("Invalid base64 data.")

        if file is None:
            raise exceptions.InvalidInput("Either 'file' or 'base64_data' must be provided.")

        if chunk <= 0:
            raise exceptions.InvalidInput("'chunk' must be a positive integer.")

        original_url = None
        if isinstance(file, str):
            if file.startswith(('http://', 'https://')):
                original_url = file
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            original_url,
                            timeout=aiohttp.ClientTimeout(total=30)
                        ) as resp:
                            if resp.status >= 500:
                                raise exceptions.ServerError(
                                    f"Server error while downloading URL: {resp.status}"
                                )
                            file = await resp.read()
                except asyncio.TimeoutError:
                    raise exceptions.TimeoutError("Timeout while downloading URL.") from None
                file_name = file_name or original_url.split('/')[-1].split('?')[0]
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

        if not mime:
            if file_name and '.' in file_name:
                mime = file_name.split('.')[-1]
            else:
                mime = "bin"

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
                        timeout=aiohttp.ClientTimeout(total=60)
                    ) as response:
                        if response.status >= 500:
                            raise exceptions.ServerError()
                        return await response.json()
                except (aiohttp.ServerTimeoutError, asyncio.TimeoutError) as e:
                    self.logger.warning(
                        f"Chunk {part_number} timeout (attempt {attempt + 1}/{max_retries}): {e}"
                    )
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                    else:
                        raise exceptions.TimeoutError("Timeout while uploading chunk.")
                except exceptions.ServerError:
                    self.logger.warning(
                        f"Chunk {part_number} server error (attempt {attempt + 1}/{max_retries})"
                    )
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                    else:
                        raise
                except Exception as e:
                    self.logger.warning(
                        f"Chunk {part_number} upload failed (attempt {attempt + 1}/{max_retries}): {e}"
                    )
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                    else:
                        raise

        result = await self.request_send_file(file_name, file_size, mime)

        if isinstance(result, dict):
            result = Data(result)

        file_id = result.id
        dc_id = result.dc_id
        upload_url = result.upload_url
        access_hash_send = result.access_hash_send

        total_parts = (file_size + chunk - 1) // chunk

        if total_parts == 0:
            result_dict = {
                "status": "OK",
                "mime": mime,
                "size": 0,
                "dc_id": dc_id,
                "file_id": file_id,
                "file_name": file_name,
                "access_hash_rec": None
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

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
                if isinstance(result, dict):
                    result = Data(result)
                file_id = result.id
                dc_id = result.dc_id
                upload_url = result.upload_url
                access_hash_send = result.access_hash_send
                index = 0
                continue

            await handle_callback(file_size, min((index + 1) * chunk, file_size))
            index += 1

        if upload_result is None:
            raise exceptions.NoConnection(
                "Upload failed: no response from server (network error)."
            )

        if upload_result.get("status") == "OK" and upload_result.get("status_det") == "OK":
            result_dict = {
                "status": "OK",
                "mime": mime,
                "size": file_size,
                "dc_id": dc_id,
                "file_id": file_id,
                "file_name": file_name,
                "access_hash_rec": upload_result["data"]["access_hash_rec"],
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        error_type = upload_result.get("status_det") or "UnknownError"
        if hasattr(exceptions, error_type):
            raise getattr(exceptions, error_type)(upload_result)
        else:
            raise exceptions.InvalidInput(f"Upload failed: {upload_result}")