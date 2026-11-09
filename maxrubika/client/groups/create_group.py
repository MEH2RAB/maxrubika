from pathlib import Path
from typing import Union, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CreateGroup:
    async def create_group(
        self: "maxrubika.Messenger",
        title: str,
        members: Union[str, List[str]],
        description: Optional[str] = None,
        avatar: Optional[Union[Path, str, bytes]] = None,
        thumbnail_avatar: Optional[Union[Path, str, bytes]] = None,
        main_file_id: Optional[Union[str, int]] = None,
        thumbnail_file_id: Optional[Union[str, int]] = None,
        *args, **kwargs
    ):
        """
        Create a new group.

        Parameters:
            title (str): The title of the group.
            members (Union[str, List[str]]): A single member GUID/Username or a list of member GUIDs/Usernames.
            description (str, optional): Description of the group.
            avatar (Path | str | bytes, optional): The image to be used as the group avatar.
            thumbnail_avatar (Path | str | bytes, optional): The image to be used as the group thumbnail avatar.
            main_file_id (Union[str, int], optional): Pre-uploaded main avatar file ID.
            thumbnail_file_id (Union[str, int], optional): Pre-uploaded thumbnail avatar file ID.

        Returns:
            The result of the API call.

        Note:
            If a file ID is provided, the corresponding image is not uploaded.
            If no thumbnail is provided, it is taken from the main image.
        """
        from ..exceptions import InvalidInput

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
                message = f"'{member}' does not point to a valid member. Expected a user GUID, bot GUID, or username."
                raise InvalidInput(message)

            member_guids.append(guid)

        input_data = {
            'title': title.strip(),
            'member_guids': member_guids,
            'description': description
        }

        if not main_file_id and avatar is not None:
            if isinstance(avatar, (str, Path)):
                kwargs['file_name'] = kwargs.get(
                    'file_name',
                    str(avatar).split('/')[-1]
                )
            else:
                kwargs['file_name'] = kwargs.get('file_name', 'maxrubika.jpg')

            upload = await self.upload_file(avatar, *args, **kwargs)
            main_file_id = upload.file_id

        if not thumbnail_file_id and main_file_id:
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
                thumbnail_file_id = main_file_id

        if main_file_id:
            input_data['main_file_id'] = main_file_id

        if thumbnail_file_id:
            input_data['thumbnail_file_id'] = thumbnail_file_id

        return await self.request(method='addGroup', input=input_data)