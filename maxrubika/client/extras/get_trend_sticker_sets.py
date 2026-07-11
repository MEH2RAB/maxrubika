import maxrubika

class GetTrendStickerSets:
    async def get_trend_sticker_sets(self: "maxrubika.Client", start_id: str = None):
        """
        Get trending sticker sets.

        Parameters:
            start_id (str): The start ID for pagination.

        Returns:
            Trending sticker sets.
        """
        return await self.request(
            method = 'getTrendStickerSets',
            input = {'start_id': start_id}
        )