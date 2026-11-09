from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RequestSendFile:
    async def request_send_file(
        self: "maxrubika.Rubino",
        file_name: str,
        file_size: int,
        file_type: Literal["Picture", "Video"] = "Picture",
        mime: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Request an upload session from Rubino servers.

        Parameters:
            file_name (str): The name of the file to be uploaded.
            file_size (int): Total file size in bytes.
            file_type (Literal["Picture", "Video"]): Either 'Picture' or 'Video'. Case-insensitive. Accepts 'Picture', 'Image', 'Photo' for Picture and 'Video', 'Clip' for Video. Defaults to 'Picture'.
            mime (str, optional): MIME type of the file. Defaults based on file_type ('jpg' for Picture, 'mp4' for Video). Only used in api_version=1.
            my_profile (str, optional): The profile that uploads. Defaults to self.profile_id.

        Returns:
            A dict containing upload endpoint, file ID, and access hash.

        Raises:
            InvalidInput: If file_type is invalid.
        """
        from .exceptions import InvalidInput

        file_type_map = {
            'picture': 'Picture',
            'image': 'Picture',
            'photo': 'Picture',
            'video': 'Video',
            'clip': 'Video'
        }

        normalized_file_type = file_type_map.get(str(file_type).lower())

        if not normalized_file_type:
            message = "'file_type' must be 'Picture' (or 'Image', 'Photo') or 'Video' (or 'Clip')."
            raise InvalidInput(message)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'file_name': file_name,
            'file_size': str(file_size),
            'file_type': normalized_file_type,
            'profile_id': profile_id
        }

        if self.api_version == 1:
            input_data['mime'] = mime or ('jpg' if normalized_file_type == 'Picture' else 'mp4')
            method = 'requestSendFile'
        else:
            method = 'requestUploadFile'

        return await self.request(
            method=method,
            input=input_data
        )