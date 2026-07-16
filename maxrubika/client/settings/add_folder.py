from typing import Union, List, Optional
import maxrubika
from ..exceptions import InvalidInput

class AddFolder:
    async def add_folder(
        self: "maxrubika.Client",
        name: str,
        include_chats: Optional[Union[str, List[str]]] = None,
        exclude_chats: Optional[Union[str, List[str]]] = None,
        include_chat_types: Optional[List[str]] = None,
        exclude_chat_types: Optional[List[str]] = None,
        is_add_to_top: bool = True,
        suggestion_folder_id: str = None,
        folder_id: str = None
    ):
        """
        Add a new folder to organize chats.

        Parameters:
            name (str): Folder name.
            include_chats: Chats (GUIDs, links, usernames) to include in folder.
            exclude_chats: Chats (GUIDs, links, usernames) to exclude from folder.
            include_chat_types: Chat types to include (e.g., ['User', 'Group', 'Channel', 'Bot']).
            exclude_chat_types: Chat types to exclude.
            is_add_to_top (bool): Add folder to top of list.
            suggestion_folder_id (str): Suggestion folder ID.
            folder_id (str): Folder ID.

        Returns:
            The result of the API call.
        """
        include_object_guids = []
        exclude_object_guids = []
        updated_parameters = []

        if include_chats is not None:
            if isinstance(include_chats, str):
                include_chats = [include_chats]
            for chat in include_chats:
                include_object_guids.append(await self.get_guid(chat))
            updated_parameters.append('include_object_guids')

        if exclude_chats is not None:
            if isinstance(exclude_chats, str):
                exclude_chats = [exclude_chats]
            for chat in exclude_chats:
                exclude_object_guids.append(await self.get_guid(chat))
            updated_parameters.append('exclude_object_guids')

        if not include_object_guids and not exclude_object_guids and not include_chat_types and not exclude_chat_types:
            raise InvalidInput(
                "At least one of 'include_chats', 'exclude_chats', "
                "'include_chat_types', or 'exclude_chat_types' must be provided."
            )

        input = {
            'name': name,
            'is_add_to_top': is_add_to_top,
            'updated_parameters': updated_parameters
        }

        if include_object_guids:
            input['include_object_guids'] = include_object_guids
        if exclude_object_guids:
            input['exclude_object_guids'] = exclude_object_guids
        if include_chat_types:
            input['include_chat_types'] = include_chat_types
            updated_parameters.append('include_chat_types')
        if exclude_chat_types:
            input['exclude_chat_types'] = exclude_chat_types
            updated_parameters.append('exclude_chat_types')
        if suggestion_folder_id:
            input['suggestion_folder_id'] = suggestion_folder_id
            updated_parameters.append('suggestion_folder_id')
        if folder_id:
            input['folder_id'] = folder_id
            updated_parameters.append('folder_id')

        return await self.request(method = 'addFolder', input = input)