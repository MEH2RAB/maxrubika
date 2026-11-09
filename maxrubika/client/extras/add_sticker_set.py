from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AddStickerSet:
    async def add_sticker_set(
        self: "maxrubika.Messenger",
        sticker_set_id: str
    ):
        """
        Add a sticker set.

        Parameters:
            sticker_set_id (str): The ID of the sticker set.

        Returns:
            The result of the API call.
        """
        input_data = {
            'sticker_set_id': sticker_set_id,
            'action': 'Add'
        }
        return await self.request(
            method='actionOnStickerSet',
            input=input_data
        )