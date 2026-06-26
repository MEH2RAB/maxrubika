from typing import Literal
import maxrubika
from .exceptions import InvalidInput, InvalidAccess

class RequestSendFile:
    async def request_send_file(
        self: "maxrubika.Bot",
        file_type: Literal['File', 'Image', 'Voice', 'Video', 'Music', 'Gif'] = 'File'
    ) -> str:
        """
        Request an upload URL for sending a file to the server.

        Parameters:
            file_type (str): Type of file to upload.
                Options: 'File', 'Image', 'Voice', 'Video', 'Music', 'Gif'.
                Defaults to 'File'.

        Returns:
            str: Upload URL for the file.

        Examples:
            # Get upload URL for an image
            upload_url = await bot.request_send_file(file_type="Image")

            # Then upload file using that URL
            file_id = await bot.upload_file(upload_url, "photo.jpg")
        """
        valid_types = ['File', 'Image', 'Voice', 'Video', 'Music', 'Gif']
        if file_type not in valid_types:
            message = f"Invalid 'file_type'. Must be one of: {valid_types}"
            raise InvalidInput(message)

        payload = {'type': file_type}
        result = await self._request('POST', 'requestSendFile', json = payload)

        try:
            return result["data"]["upload_url"]

        except KeyError:
            raise InvalidAccess("Failed to get upload URL.")