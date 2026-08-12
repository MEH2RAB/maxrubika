from typing import Optional, Union, List
import maxrubika
from ..exceptions import InvalidInput

VALID_FILTER_TYPES = {'User', 'Channel', 'Bot'}

class SearchGlobalChats:
    async def search_global_chats(
        self: "maxrubika.Client",
        text: str,
        filter_type: Optional[Union[str, List[str]]] = None,
        start_id: Optional[str] = None
    ):
        """
        Search for global chats (users, channels, etc.) based on the given search text.

        Parameters:
            text (str): The text to search for.
            filter_type (str or list, optional): Filter results by type. 
                'User', 'Channel', 'Bot' or a list of them.
            start_id (str, optional): The ID to start fetching from. Defaults to None.

        Returns:
            The update containing search results.
        """
        input = {'search_text': text}

        if filter_type:
            if isinstance(filter_type, str):
                filter_type = [filter_type]
            
            for ft in filter_type:
                if ft not in VALID_FILTER_TYPES:
                    raise InvalidInput(
                        f"Invalid filter_type: '{ft}'. Must be one of: {', '.join(sorted(VALID_FILTER_TYPES))}"
                    )
            
            input['filter_types'] = filter_type

        if start_id:
            input['start_id'] = start_id

        return await self.request(
            method='searchGlobalObjects',
            input=input
        )