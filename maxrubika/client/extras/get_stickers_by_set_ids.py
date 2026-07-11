from typing import Union
import maxrubika

class GetStickersBySetIDs:
    async def get_stickers_by_set_ids(
        self: "maxrubika.Client",
        sticker_set_ids: Union[str, list]
    ):
        """
        Get stickers by set IDs.

        Parameters:
            sticker_set_ids (Union[str, list]): The sticker set ID or a list of sticker set IDs.

        Returns:
            Stickers corresponding to the provided set IDs.
        """
        if isinstance(sticker_set_ids, str):
            sticker_set_ids = [str(sticker_set_ids)]

        return await self.request(method = 'GetStickersBySetIDs', input = {'sticker_set_ids': sticker_set_ids})