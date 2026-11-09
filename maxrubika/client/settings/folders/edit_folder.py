from typing import Union, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class EditFolder:
    async def edit_folder(
        self: "maxrubika.Messenger",
        folder_id: str,
        name: Optional[str] = None,
        include_chats: Optional[Union[str, List[str]]] = None,
        exclude_chats: Optional[Union[str, List[str]]] = None,
        include_chat_types: Optional[List[str]] = None,
        exclude_chat_types: Optional[List[str]] = None,
        is_add_to_top: Optional[bool] = None
    ):
        """
        Edit an existing folder.

        Parameters:
            folder_id (str): The ID of the folder to edit.
            name (str, optional): New folder name.
            include_chats (Union[str, List[str]], optional): Chats to include.
            exclude_chats (Union[str, List[str]], optional): Chats to exclude.
            include_chat_types (List[str], optional): Chat types to include.
            exclude_chat_types (List[str], optional): Chat types to exclude.
            is_add_to_top (bool, optional): Add folder to top of list.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput
        from .add_folder import _normalize_include_chat_type, _normalize_exclude_chat_type

        include_object_guids = []
        exclude_object_guids = []
        updated_parameters = []

        if name is not None:
            updated_parameters.append('name')

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

        normalized_include_types = None
        if include_chat_types:
            normalized_include_types = []
            for ct in include_chat_types:
                normalized_include_types.extend(_normalize_include_chat_type(ct))
            normalized_include_types = list(dict.fromkeys(normalized_include_types))
            updated_parameters.append('include_chat_types')

        normalized_exclude_types = None
        if exclude_chat_types:
            normalized_exclude_types = []
            for ct in exclude_chat_types:
                normalized_exclude_types.extend(_normalize_exclude_chat_type(ct))
            normalized_exclude_types = list(dict.fromkeys(normalized_exclude_types))
            updated_parameters.append('exclude_chat_types')

        if is_add_to_top is not None:
            updated_parameters.append('is_add_to_top')

        if not updated_parameters:
            raise InvalidInput("At least one of 'name', 'include_chats', 'exclude_chats', 'include_chat_types', 'exclude_chat_types', or 'is_add_to_top' must be provided.")

        input_data = {
            'folder_id': folder_id,
            'updated_parameters': updated_parameters,
        }

        if name is not None:
            input_data['name'] = name
        if include_object_guids:
            input_data['include_object_guids'] = include_object_guids
        if exclude_object_guids:
            input_data['exclude_object_guids'] = exclude_object_guids
        if normalized_include_types:
            input_data['include_chat_types'] = normalized_include_types
        if normalized_exclude_types:
            input_data['exclude_chat_types'] = normalized_exclude_types
        if is_add_to_top is not None:
            input_data['is_add_to_top'] = is_add_to_top

        return await self.request(method='editFolder', input=input_data)