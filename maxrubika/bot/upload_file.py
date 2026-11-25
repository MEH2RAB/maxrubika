import os
import asyncio
import logging
import mimetypes
import base64 as b64
from typing import Optional, Union, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import aiohttp
    import maxrubika

logger = logging.getLogger(__name__)

class UploadFile:
    async def upload_file(
        self: "maxrubika.Bot",
        file: Optional[Union[str, bytes]] = None,
        base64: Optional[str] = None,
        file_name: Optional[str] = None,
        file_type: Optional[Literal['File', 'Image', 'Voice', 'Video', 'Music', 'Gif']] = None
    ) -> Optional[str]:
        """
        Upload a file to the server and return file_id.

        Automatically requests an upload URL via `request_send_file`, then uploads
        the file in a single request.

        Supports local path, URL, raw bytes, and base64.

        Parameters:
            file (str | bytes, optional): Path, URL, or raw bytes.
            base64 (str, optional): Base64-encoded file data.
            file_name (str, optional): Name of the file. Auto-detected when possible.
            file_type (Literal['File', 'Image', 'Voice', 'Video', 'Music', 'Gif'], optional):
                Type of file. If not provided, auto-detected from the file extension. Defaults to 'File'.

        Returns:
            Optional[str]: file_id or None if failed.
        """
        import aiohttp
        from .exceptions import APIException, BadGateway, ServerError, InvalidInput, Timeout
        from .file_extensions import _get_file_type

        if base64:
            try:
                file = b64.b64decode(base64)
            except Exception:
                raise InvalidInput("Invalid base64 data.")

        if file is None:
            raise InvalidInput("Either 'file' or 'base64' must be provided.")

        is_path = isinstance(file, str) and not file.startswith(("http://", "https://"))

        if isinstance(file, str):
            if file.startswith(("http://", "https://")):
                file = await self._download_url(file)
                file_name = file_name or "file.bin"
            elif is_path:
                file_name = file_name or os.path.basename(file)

        elif isinstance(file, bytes):
            if not file_name:
                raise InvalidInput("'file_name' required for bytes/base64 uploads.")
        else:
            raise InvalidInput("Expected str (path/URL) or bytes.")

        if file_type is None:
            file_type = _get_file_type(file_name)

        if is_path:
            import aiofiles
            async with aiofiles.open(file, "rb") as f:
                file_data = await f.read()
        else:
            file_data = file

        file_size = len(file_data)
        if file_size == 0:
            raise InvalidInput("File is empty.")

        content_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
        session = await self._get_session()

        url = await self.request_send_file(file_type=file_type)

        logger.info(f"Uploading {file_name} ({file_size} bytes) as {file_type}...")

        for attempt in range(self.max_retries):
            try:
                form = aiohttp.FormData(quote_fields=False)
                form.add_field(
                    "file", file_data,
                    filename=file_name,
                    content_type=content_type,
                )
                timeout = aiohttp.ClientTimeout(total=180)

                async with session.post(url, data=form, timeout=timeout) as response:
                    if response.status == 502:
                        raise BadGateway(dev_message="Server unavailable (502).")
                    if response.status == 500:
                        raise ServerError(dev_message="Server error (500).")
                    if response.status != 200:
                        text = await response.text()
                        raise APIException(
                            status=f"HTTP_{response.status}",
                            dev_message=f"HTTP {response.status}: {text[:500]}")

                    data = await response.json()
                    if data.get("status") != "OK":
                        raise APIException.from_response(data)

                    file_id = data.get("data", {}).get("file_id")
                    if not file_id:
                        raise APIException(
                            status="NO_FILE_ID",
                            dev_message="Server did not return file_id."
                        )

                    logger.info(f"Uploaded {file_name} successfully.")
                    return file_id

            except (APIException, ServerError):
                raise

            except (BadGateway, asyncio.TimeoutError, aiohttp.ClientError) as e:
                if attempt >= self.max_retries - 1:
                    if isinstance(e, asyncio.TimeoutError):
                        raise Timeout(dev_message="Upload timed out.") from None
                    raise e from None
                wait = 2 ** attempt
                logger.warning(
                    f"Upload failed - Attempt {attempt + 1}/{self.max_retries}: {type(e).__name__} - Retry in {wait}s...")
                await asyncio.sleep(wait)

        return None

    async def _download_url(self, url: str) -> bytes:
        from .exceptions import InvalidInput

        session = await self._get_session()
        logger.info(f"Downloading from {url}...")
        async with session.get(url) as resp:
            if resp.status != 200:
                raise InvalidInput(f"Failed to download file: HTTP {resp.status}")
            data = await resp.read()
        logger.info(f"Downloaded {len(data)} bytes.")
        return data