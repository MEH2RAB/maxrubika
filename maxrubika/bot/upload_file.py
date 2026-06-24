import aiohttp
import asyncio
from pathlib import Path
from typing import Optional, Union
import maxrubika
from .exceptions import APIException

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

        for attempt in range(1, 6):
            try:
                if attempt == 1:
                    print(f"Uploading {file_name}...")
                else:
                    print(f"Retry {attempt}/5: {file_name}")

                form = aiohttp.FormData()
                form.add_field(
                    "file",
                    file_path.read_bytes(),
                    filename=file_name,
                    content_type="application/octet-stream"
                )

                connector = aiohttp.TCPConnector(ssl=False)
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.post(url, data=form) as response:
                        if response.status != 200:
                            if response.status >= 500 and attempt < 5:
                                wait = 2 ** attempt
                                print(f"Server error {response.status}, retrying in {wait}s...")
                                await asyncio.sleep(wait)
                                continue
                            text = await response.text()
                            raise aiohttp.ClientResponseError(
                                response.request_info,
                                response.history,
                                status=response.status,
                                message=text
                            )

                        data = await response.json()
                        if data.get("status") != "OK":
                            raise APIException.from_response(data)

                        file_id = data["data"]["file_id"]
                        return file_id

            except APIException:
                raise
            except aiohttp.ClientResponseError as e:
                if attempt == 5:
                    raise
                if e.status >= 500:
                    print(f"Error: {e}, retrying...")
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise
            except Exception as e:
                if attempt == 5:
                    raise
                print(f"Error: {e}, retrying...")
                await asyncio.sleep(2 ** attempt)

        return None