from pathlib import Path
from typing import Union, List, Optional
import maxrubika
from ..exceptions import InvalidInput

class CreateGroup:
    async def create_group(
        self: "maxrubika.Client",
        title: str,
        members: Union[str, List[str]],
        description: Optional[str] = None,
        avatar: Optional[Union[Path, str, bytes]] = None,
        thumbnail_avatar: Optional[Union[Path, str, bytes]] = None,
        *args, **kwargs
    ):
        """
        Create a new group.

        Parameters:
            title (str): The title of the group.
            members (Union[str, List[str]]): A single member GUID/Username or a list of member GUIDs/Usernames to be added to the group.
            description (Optional[str]): Description of the group (optional). Defaults to None.
            avatar (Optional[Union[Path, str, bytes]]): The image to be used as the group avatar. Default is None.
            thumbnail_avatar (Optional[Union[Path, str, bytes]]): The image to be used as the group thumbnail avatar. Default is None.

        Returns:
            The result of the API call.

        Note:
            If only `avatar` is provided, the thumbnail is taken from the same image.
            If none of them are provided, no avatar is set for the group.
        """
        if isinstance(members, str):
            members = [members]

        if not members:
            raise InvalidInput("At least one member is required to create a group.")

        if len(title) > 60:
            raise InvalidInput("Title cannot exceed 60 characters.")
        if len(title) == 0:
            raise InvalidInput("Title cannot be empty.")

        if description is not None:
            if len(description) > 300:
                raise InvalidInput("Description cannot exceed 300 characters.")

        member_guids = []

        for member in members:
            guid = await self.get_guid(member)

            if not guid.startswith(("u0", "b0")):
                message = (
                    f"'{member}' does not point to a valid member. "
                    "Expected a user GUID, bot GUID, or username."
                )
                raise InvalidInput(message)

            member_guids.append(guid)

        input_data = {
            'title': title.strip(),
            'member_guids': member_guids,
            'description': description
        }

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

        return await self.request(method = 'addGroup', input = input_data)