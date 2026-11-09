from typing import Optional, Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

VALID_FILTER_TYPES = {'User', 'Channel', 'Bot'}

class SearchGlobalChats:
    async def search_global_chats(
        self: "maxrubika.Messenger",
        text: str,
        filter_type: Optional[Union[str, List[str]]] = None,
        start_id: Optional[str] = None
    ):
        """
        Search for global chats (users, channels, etc.) based on the given search text.

        Parameters:
            text (str): The text to search for.
            filter_type (Union[str, List[str]], optional): 'User', 'Channel', 'Bot' or a list of them. Case-insensitive.
            start_id (str, optional): The ID to start fetching from. Defaults to None.

        Returns:
            The update containing search results.
        """
        from ...exceptions import InvalidInput

        filter_type_map = {
            'user': 'User',
            'channel': 'Channel',
            'bot': 'Bot'
        }

        input_data = {'search_text': text}

        if filter_type:
            if isinstance(filter_type, str):
                filter_type = [filter_type]

            normalized_filter_types = []

            for ft in filter_type:
                normalized = filter_type_map.get(str(ft).lower())

                if not normalized:
                    message = f"Invalid filter_type: '{ft}'. Must be one of: {', '.join(sorted(VALID_FILTER_TYPES))}"
                    raise InvalidInput(message)

                normalized_filter_types.append(normalized)

            input_data['filter_types'] = normalized_filter_types

        if start_id:
            input_data['start_id'] = start_id

        return await self.request(
            method='searchGlobalObjects',
            input=input_data
        )