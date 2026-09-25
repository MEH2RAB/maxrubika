from typing import List, Union
import maxrubika
from ..exceptions import InvalidInput

class ReorderStickerSets:
    async def reorder_sticker_sets(
        self: "maxrubika.Client",
        ordered_sticker_set_ids: Union[str, List[str]]
    ):
        """
        Reorder sticker sets in the user's collection.

        Parameters:
            ordered_sticker_set_ids (Union[str, List[str]]): A single sticker
                set ID or a list of sticker set IDs in the desired order.

        Returns:
            The result of the API call.
        """
        if isinstance(ordered_sticker_set_ids, str):
            ordered_sticker_set_ids = [ordered_sticker_set_ids]

        return await self.request(
            method = 'reorderStickerSets',
            input = {
                'ordered_sticker_set_ids': ordered_sticker_set_ids
            }
        )