import aiohttp
import asyncio
import logging
from typing import Optional
import maxrubika
from .exceptions import APIException, BadGateway, ServerError, InvalidInput

logger = logging.getLogger(__name__)

class UploadFile:
    async def upload_file(
        self: "maxrubika.Bot",
        url: str,
        file_name: Optional[str] = None,
        file_bytes: Optional[bytes] = None
    ) -> Optional[str]:
        """
        Upload a file to the server and return file_id.

        Parameters:
            url (str): Upload URL from request_send_file.
            file_name (str, optional): Name of the file sent to server.
            file_bytes (bytes, optional): Raw bytes of the file to upload.

        Returns:
            Optional[str]: file_id or None if failed.
        """
        if file_bytes is None:
            raise InvalidInput("'file_bytes' must be provided")

        if file_name is None:
            file_name = "file.bin"

        session = await self._get_session()

        for attempt in range(self.max_retries):
            try:
                if attempt == 0:
                    logger.info(f"Uploading {file_name}...")

                form = aiohttp.FormData(quote_fields=False)
                form.add_field(
                    "file",
                    file_bytes,
                    filename=file_name,
                    content_type="application/octet-stream"
                )
                async with session.post(url, data=form) as response:
                    if response.status == 502:
                        raise BadGateway(
                            dev_message="Upload failed: Server temporarily unavailable (502)."
                        )

                    if response.status == 500:
                        raise ServerError(
                            dev_message="Upload failed: Server error (500)."
                        )

                    if response.status != 200:
                        text = await response.text()
                        raise APIException(
                            status=f"HTTP_{response.status}",
                            dev_message=f"HTTP {response.status}: {text[:500]}"
                        )

                    data = await response.json()
                    if data.get("status") != "OK":
                        raise APIException.from_response(data)

                    file_id = data["data"]["file_id"]
                    return file_id

            except BadGateway as e:
                if attempt < self.max_retries - 1:
                    wait = 2 ** attempt
                    logger.warning(f"Upload failed - Attempt {attempt + 1}/{self.max_retries}: {type(e).__name__} - Retry in {wait}s...")
                    await asyncio.sleep(wait)
                    continue
                raise

            except APIException:
                raise

            except asyncio.TimeoutError:
                if attempt < self.max_retries - 1:
                    wait = 2 ** attempt
                    logger.warning(f"Upload failed - Attempt {attempt + 1}/{self.max_retries}: Timeout - Retry in {wait}s...")
                    await asyncio.sleep(wait)
                    continue
                raise

            except Exception as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Upload failed - Attempt {attempt + 1}/{self.max_retries}: {type(e).__name__} - Retry...")
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise

        return None