from pathlib import Path
from typing import Union, Optional
import maxrubika
from ..exceptions import InvalidInput

class CreateChannel:
    async def create_channel(
        self: "maxrubika.Client",
        title: str,
        members: Optional[Union[str, list]] = None,
        channel_type: str = 'Public',
        description: Optional[str] = None,
        avatar: Optional[Union[Path, str, bytes]] = None,
        thumbnail_avatar: Optional[Union[Path, str, bytes]] = None,
        *args, **kwargs
    ):
        """
        Create a new channel.

        Parameters:
            title (str): The title of the new channel.
            members (Union[str, list], optional): The GUID(s) or username(s) of the member(s) to be added to the new channel. Default is None.
            channel_type (str): Set type of the channel. 'Public' or 'Private'. Default is 'Public'.
            description (str, optional): The description of the new channel. Default is None.
            avatar (Optional[Union[Path, str, bytes]]): The image to be used as the channel avatar. Default is None.
            thumbnail_avatar (Optional[Union[Path, str, bytes]]): The image to be used as the channel thumbnail avatar. Default is None.

        Returns:
            The result of the API call.

        Note:
            If only `avatar` is provided, the thumbnail is taken from the same image.
            If none of them are provided, no avatar is set for the channel.
        """
        if len(title) > 60:
            raise InvalidInput("Title cannot exceed 60 characters.")
        if len(title) == 0:
            raise InvalidInput("Title cannot be empty.")

        if channel_type not in ('Public', 'Private'):
            raise InvalidInput("'channel_type' must be either 'Public' or 'Private'.")

        if description is not None:
            if len(description) > 300:
                raise InvalidInput("Description cannot exceed 300 characters.")

        input_data = {
            'title': title,
            'description': description,
            'channel_type': channel_type
        }

        member_guids = []
        if members is not None:
            if isinstance(members, str):
                members = [members]

            for member in members:
                guid = await self.get_guid(member)

                if not guid.startswith(("u0", "b0")):
                    message = (
                        f"'{member}' does not point to a valid member. "
                        "Expected a user GUID, bot GUID, or username."
                    )
                    raise InvalidInput(message)

                member_guids.append(guid)

            input_data['member_guids'] = member_guids

        if avatar is not None:
            if isinstance(avatar, (str, Path)):
                kwargs['file_name'] = kwargs.get(
                    'file_name',
                    str(avatar).split('/')[-1]
                )
            else:
                kwargs['file_name'] = kwargs.get('file_name', 'maxrubika.jpg')

            upload = await self.upload_file(avatar, *args, **kwargs)

            if thumbnail_avatar is not None:
                if isinstance(thumbnail_avatar, (str, Path)):
                    kwargs['file_name'] = kwargs.get(
                        'file_name',
                        str(thumbnail_avatar).split('/')[-1]
                    )
                else:
                    kwargs['file_name'] = kwargs.get('file_name', 'maxrubika.jpg')

                upload_thumb = await self.upload_file(thumbnail_avatar, *args, **kwargs)
                thumbnail_file_id = upload_thumb.file_id
            else:
                thumbnail_file_id = upload.file_id

            input_data['main_file_id'] = upload.file_id
            input_data['thumbnail_file_id'] = thumbnail_file_id

        return await self.request(method = 'addChannel', input = input_data)