from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SearchStickers:
    async def search_stickers(
        self: "maxrubika.Messenger",
        search_text: str = '',
        start_id: Optional[str] = None
    ):
        """
        Search for stickers.

        Parameters:
            search_text (str): The search text.
            start_id (str, optional): The start ID for pagination. Defaults to None.

        Returns:
            Stickers matching the search criteria.
        """
        input_data = {'search_text': search_text}

        if start_id:
            input_data['start_id'] = start_id

        return await self.request(
            method='searchStickers',
            input=input_data
        )