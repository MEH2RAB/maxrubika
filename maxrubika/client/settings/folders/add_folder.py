from typing import Union, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

VALID_INCLUDE_CHAT_TYPES = {
    'Contacts', 'NonConatcts', 'Groups', 'Channels', 'Bots', 'Services'
}
VALID_EXCLUDE_CHAT_TYPES = {'Mute', 'Read', 'Archive'}

INCLUDE_CHAT_TYPE_ALIASES = {
    'contacts': ['Contacts'],
    'noncontacts': ['NonConatcts'],
    'nonconatcts': ['NonConatcts'],
    'users': ['Contacts', 'NonConatcts'],
    'groups': ['Groups'],
    'channels': ['Channels'],
    'bots': ['Bots'],
    'services': ['Services'],
}

EXCLUDE_CHAT_TYPE_ALIASES = {
    'mute': ['Mute'],
    'muted': ['Mute'],
    'read': ['Read'],
    'archive': ['Archive'],
    'archived': ['Archive'],
}

def _normalize_include_chat_type(value: str) -> list:
    from ...exceptions import InvalidInput

    if not isinstance(value, str):
        raise InvalidInput(f"Invalid include chat type: {value!r}")

    key = value.strip().lower()
    if key in INCLUDE_CHAT_TYPE_ALIASES:
        return INCLUDE_CHAT_TYPE_ALIASES[key]

    message = f"Invalid include chat type: '{value}'. Must be one of: {', '.join(sorted(VALID_INCLUDE_CHAT_TYPES))}"
    raise InvalidInput(message)

def _normalize_exclude_chat_type(value: str) -> list:
    from ...exceptions import InvalidInput

    if not isinstance(value, str):
        raise InvalidInput(f"Invalid exclude chat type: {value!r}")

    key = value.strip().lower()
    if key in EXCLUDE_CHAT_TYPE_ALIASES:
        return EXCLUDE_CHAT_TYPE_ALIASES[key]

    message = f"Invalid exclude chat type: '{value}'. Must be one of: {', '.join(sorted(VALID_EXCLUDE_CHAT_TYPES))}"
    raise InvalidInput(message)

class AddFolder:
    async def add_folder(
        self: "maxrubika.Messenger",
        name: str,
        include_chats: Optional[Union[str, List[str]]] = None,
        exclude_chats: Optional[Union[str, List[str]]] = None,
        include_chat_types: Optional[List[str]] = None,
        exclude_chat_types: Optional[List[str]] = None,
        is_add_to_top: bool = True,
        suggestion_folder_id: Optional[str] = None
    ):
        """
        Add a new folder to organize chats.

        Parameters:
            name (str): Folder name.
            include_chats (Union[str, List[str]], optional): Chats (GUIDs, links, usernames) to include.
            exclude_chats (Union[str, List[str]], optional): Chats to exclude.
            include_chat_types (List[str], optional): Chat types to include (case-insensitive): 'Contacts', 'NonContacts'/'Users', 'Groups', 'Channels', 'Bots', 'Services'.
            exclude_chat_types (List[str], optional): Chat types to exclude (case-insensitive): 'Mute', 'Read', 'Archive'.
            is_add_to_top (bool): Add folder to top of list.
            suggestion_folder_id (str, optional): Suggestion folder ID.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

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

        if (
            not include_object_guids
            and not exclude_object_guids
            and not include_chat_types
            and not exclude_chat_types
        ):
            raise InvalidInput("At least one of 'include_chats', 'exclude_chats', 'include_chat_types', or 'exclude_chat_types' must be provided.")

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

        if suggestion_folder_id:
            updated_parameters.append('suggestion_folder_id')

        input_data = {
            'name': name,
            'is_add_to_top': is_add_to_top,
            'updated_parameters': updated_parameters,
        }

        if include_object_guids:
            input_data['include_object_guids'] = include_object_guids
        if exclude_object_guids:
            input_data['exclude_object_guids'] = exclude_object_guids
        if normalized_include_types:
            input_data['include_chat_types'] = normalized_include_types
        if normalized_exclude_types:
            input_data['exclude_chat_types'] = normalized_exclude_types
        if suggestion_folder_id:
            input_data['suggestion_folder_id'] = suggestion_folder_id

        return await self.request(method='addFolder', input=input_data)