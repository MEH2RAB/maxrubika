from typing import Optional
import maxrubika

class SearchGlobalMessages:
    async def search_global_messages(
        self: "maxrubika.Client",
        search_text: str,
        start_id: Optional[str] = None,
    ):
        """
        Search for messages globally across all chats.

        Parameters:
            search_text (str): The text or hashtag to search for.
            start_id (str, optional): The ID to start fetching from. Defaults to None.

        Returns:
            The result of the API call.
        """
        is_hashtag = search_text.startswith('#')

        input = {
            'search_text': search_text[1:] if is_hashtag else search_text,
            'type': 'Hashtag' if is_hashtag else 'Text'
        }

        if start_id:
            input['start_id'] = start_id

        return await self.request(
            method = 'searchGlobalMessages',
            input = input
        )