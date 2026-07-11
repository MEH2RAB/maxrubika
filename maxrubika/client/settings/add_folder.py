import maxrubika
from typing import List, Optional
from ..exceptions import InvalidInput

class AddFolder:
    async def add_folder(
        self: "maxrubika.Client",
        name: str,
        include_object_guids: Optional[List[str]] = None,
        exclude_object_guids: Optional[List[str]] = None,
        is_add_to_top: bool = True
    ):
        """
        Add a new folder to organize chats.

        Parameters:
            name (str): Folder name.
            include_object_guids: Specific GUIDs to include in folder.
            exclude_object_guids: Specific GUIDs to exclude from folder.
            is_add_to_top (bool): Add folder to top of list.

        Returns:
            The result of the API call.
        """
        if not include_object_guids and not exclude_object_guids:
            raise InvalidInput(
                "At least one of 'include_object_guids' or 'exclude_object_guids' "
                "must be provided. Empty folders are not allowed."
            )

        input = {
            'name': name,
            'is_add_to_top': is_add_to_top
        }
        if include_object_guids is not None:
            input['include_object_guids'] = include_object_guids

        if exclude_object_guids is not None:
            input['exclude_object_guids'] = exclude_object_guids

        return await self.request(method = 'addFolder', input = input)