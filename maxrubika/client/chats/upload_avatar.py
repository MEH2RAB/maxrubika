from pathlib import Path
from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class UploadAvatar:
    async def upload_avatar(
        self: "maxrubika.Client",
        chat: str,
        main_image: Union[Path, bytes],
        thumbnail_image: Union[Path, bytes] = None,
        *args, **kwargs
    ):
        """
        Uploads an avatar image for a specified chat (user, group, or channel).

        Parameters:
            chat (str): The GUID, link, or username of the chat for which the avatar is being uploaded.
            main_image (Union[Path, bytes]): The image file or bytes to be used as the avatar.
            thumbnail_image (Union[Path, bytes]): The image file or bytes of the thumbnail image.

        Returns:
            The result of the avatar upload operation.

        Note:
            If `chat` is 'me', 'cloud', or 'self', it will be replaced with the client's GUID.
            If `image` is a string (path to a file), the file name is extracted from the path.
                Otherwise, a default file name ('maxrubika.jpg') is used.
            The `upload_file` method is used internally to handle the file upload process.
        """
        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")) and chat_guid != self.guid:
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        if isinstance(main_image, str):
            kwargs['file_name'] = kwargs.get('file_name', main_image.split('/')[-1])
        else:
            kwargs['file_name'] = kwargs.get('file_name', 'maxrubika.jpg')

        upload = await self.upload_file(main_image, *args, **kwargs)

        if thumbnail_image is not None:
            upload_thumb = await self.upload_file(thumbnail_image, *args, **kwargs)
            thumbnail_file_id = upload_thumb.file_id
        else:
            thumbnail_file_id = upload.file_id

        input = {
            'object_guid': chat_guid,
            'thumbnail_file_id': thumbnail_file_id,
            'main_file_id': upload.file_id
        }
        return await self.request(method = 'uploadAvatar', input = input)