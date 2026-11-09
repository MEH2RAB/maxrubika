from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RequestSendFile:
    async def request_send_file(
        self: "maxrubika.Bot",
        file_type: Literal['File', 'Image', 'Voice', 'Video', 'Music', 'Gif'] = 'File'
    ) -> str:
        """
        Request an upload URL for sending a file to the server.

        Parameters:
            file_type (Literal['File', 'Image', 'Voice', 'Video', 'Music', 'Gif']): Type of file to upload. Case-insensitive. Default is 'File'.

        Returns:
            str: Upload URL for the file.

        Examples:
            # Get upload URL for an image
            upload_url = await bot.request_send_file(file_type="Image")

            # Then upload file using that URL
            file_id = await bot.upload_file(upload_url, "photo.jpg")
        """
        from ..data import Data
        from .exceptions import InvalidInput, ServerError

        type_map = {
            'file': 'File',
            'image': 'Image',
            'voice': 'Voice',
            'video': 'Video',
            'music': 'Music',
            'gif': 'Gif'
        }

        normalized_type = type_map.get(file_type.lower()) if isinstance(file_type, str) else None

        if not normalized_type:
            message = "'file_type' must be 'File', 'Image', 'Voice', 'Video', 'Music', or 'Gif'."
            raise InvalidInput(message)

        result = await self.request(
            method='requestSendFile',
            input={'type': normalized_type}
        )

        if isinstance(result, dict):
            result = Data(result)

        data = result.find_keys('data')

        if isinstance(data, dict):
            data = Data(data)

        upload_url = data.find_keys('upload_url')

        if not upload_url:
            message = "Failed to get upload URL."
            raise ServerError(message)

        return upload_url