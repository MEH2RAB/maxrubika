import pathlib
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DownloadImage:
    async def download_image(
        self: "maxrubika.RubiAI",
        task_id: str,
        save_as: Optional[Union["pathlib.Path", str]] = None,
        max_wait: int = 60,
        interval: int = 2
    ):
        """
        Retrieve an AI-generated image result and optionally save it to disk.

        Polls the API until the image is ready (status: Success) or fails (status: Error).

        Parameters:
            task_id (str): Image generation/download task identifier.
            save_as (Path | str, optional): Destination path. If omitted, the decoded image is not saved.
            max_wait (int): Maximum seconds to wait for the image (polling).
            interval (int): Seconds between polls.

        Returns:
            Parsed image download response (status: Success/Error).
        """
        import asyncio
        import base64
        import aiofiles
        from ...data import Data

        result = None
        waited = 0

        while waited < max_wait:
            result = await self.request(method="downloadImage", input={"task_id": task_id})

            if isinstance(result, dict):
                result = Data(result)

            status = result.find_keys('status')

            if status == "Success":
                if save_as:
                    image_data = result.find_keys('image')
                    if image_data:
                        async with aiofiles.open(save_as, "wb") as file:
                            await file.write(base64.b64decode(image_data))
                return result

            if status == "Error":
                return result

            await asyncio.sleep(interval)
            waited += interval

        return result