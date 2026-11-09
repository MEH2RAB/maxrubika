from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteStickerSet:
    async def delete_sticker_set(
        self: "maxrubika.Messenger",
        sticker_set_id: str
    ):
        """
        Delete a sticker set.

        Parameters:
            sticker_set_id (str): The ID of the sticker set.

        Returns:
            The result of the API call.
        """
        input_data = {'sticker_set_id': sticker_set_id, 'action': 'Remove'}
        return await self.request(
            method='actionOnStickerSet',
            input=input_data
        )