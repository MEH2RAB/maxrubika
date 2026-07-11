import maxrubika

class AddStickerSet:
    async def add_sticker_set(
        self: "maxrubika.Client",
        sticker_set_id: str
    ):
        """
        Add a sticker set.

        Parameters:
            sticker_set_id (str): The ID of the sticker set.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'actionOnStickerSet',
            input = {
                'sticker_set_id': sticker_set_id,
                'action': 'Add'
                }
            )