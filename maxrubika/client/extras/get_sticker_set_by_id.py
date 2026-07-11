import maxrubika

class GetStickerSetByID:
    async def get_sticker_set_by_id(
        self: "maxrubika.Client",
        sticker_set_id: str
    ):
        """
        Get a sticker set by its ID.

        Parameters:
            sticker_set_id (str): The ID of the sticker set.

        Returns:
            The sticker set corresponding to the provided ID.
        """
        return await self.request(method = 'getStickerSetByID', input = {'sticker_set_id': sticker_set_id})