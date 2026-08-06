from typing import Optional, Literal
import maxrubika
from ..exceptions import InvalidInput

VALID_FILTER_TYPES = {'User', 'Channel', 'Bot'}

class SearchGlobalChats:
    async def search_global_chats(
        self: "maxrubika.Client",
        text: str,
        filter_type: Optional[Literal['User', 'Channel', 'Bot']] = None,
        start_id: Optional[str] = None
    ):
        """
        Search for global chats (users, channels, etc.) based on the given search text.

        Parameters:
            text (str): The text to search for.
            filter_type (str, optional): Filter results by type. 'User', 'Channel', or 'Bot'.
            start_id (str, optional): The ID to start fetching from. Defaults to None.

        Returns:
            The update containing search results.
        """
        if filter_type and filter_type not in VALID_FILTER_TYPES:
            raise InvalidInput(
                f"Invalid filter_type: '{filter_type}'. Must be one of: {', '.join(sorted(VALID_FILTER_TYPES))}"
            )

        input = {'search_text': text}

        if filter_type:
            input['filter_type'] = filter_type

        if start_id:
            input['start_id'] = start_id

        return await self.request(
            method = 'searchGlobalObjects',
            input = input
        )