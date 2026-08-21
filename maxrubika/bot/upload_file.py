import aiohttp
import asyncio
import logging
from pathlib import Path
from typing import Optional, Union
import maxrubika
from .exceptions import APIException, BadGateway, ServerError

logger = logging.getLogger(__name__)

class UploadFile:
    async def upload_file(
        self: "maxrubika.Bot",
        file_path: Union[str, Path],
        url: str,
        file_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Upload a file to the server and return file_id.

        Parameters:
            url (str): Upload URL from request_send_file.
            file_path (str/Path): Path to the file to upload.
            file_name (str, optional): Name of the file sent to server. 
                If not provided, uses file_path's filename.

        Returns:
            Optional[str]: file_id or None if failed.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_name is None:
            file_name = file_path.name

        session = await self._get_session()

        for attempt in range(self.max_retries):
            try:
                if attempt == 0:
                    logger.info(f"Uploading {file_name}...")
                else:
                    logger.warning(f"Request failed - Attempt {attempt + 1}/{self.max_retries}: {file_name} - Retry...")

                form = aiohttp.FormData(quote_fields=False)
                form.add_field(
                    "file",
                    file_path.read_bytes(),
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

            except (BadGateway, ServerError) as e:
                if attempt < self.max_retries - 1:
                    wait = 2 ** attempt
                    logger.warning(f"Request failed - Attempt {attempt + 1}/{self.max_retries}: {type(e).__name__} - Retry in {wait}s...")
                    await asyncio.sleep(wait)
                    continue
                raise

            except APIException:
                raise

            except Exception as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Request failed - Attempt {attempt + 1}/{self.max_retries}: {e} - Retry...")
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise

        return None