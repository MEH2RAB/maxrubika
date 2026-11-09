from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetTrendStickerSets:
    async def get_trend_sticker_sets(
        self: "maxrubika.Messenger",
        search_text: Optional[str] = None,
        start_id: Optional[str] = None
    ):
        """
        Get trending sticker sets.

        Parameters:
            search_text (str, optional): Search text for filtering sticker sets. Defaults to None.
            start_id (str, optional): The start ID for pagination. Defaults to None.

        Returns:
            Trending sticker sets.
        """
        input_data = {}

        if search_text:
            input_data['search_text'] = search_text

        if start_id:
            input_data['start_id'] = start_id

        return await self.request(
            method='getTrendStickerSets',
            input=input_data
        )