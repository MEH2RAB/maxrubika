import maxrubika

class SearchStickers:
    async def search_stickers(
        self: "maxrubika.Client",
        search_text: str = '',
        start_id: str = None
    ):
        """
        Search for stickers.

        Parameters:
            search_text (str): The search text.
            start_id (str): The start ID for pagination.

        Returns:
            Stickers matching the search criteria.
        """
        return await self.request(
            method = 'searchStickers',
            input = {'search_text': search_text, 'start_id': start_id})