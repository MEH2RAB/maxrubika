from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMyArchivedStickerSets:
    async def get_my_archived_sticker_sets(
        self: "maxrubika.Messenger",
        search_text: Optional[str] = None,
        start_id: Optional[str] = None
    ):
        """
        Get archived sticker sets of the current user.

        Parameters:
            search_text (str, optional): Search text for filtering sticker sets. Defaults to None.
            start_id (str, optional): The ID to start fetching from. Defaults to None.

        Returns:
            The result of the API call.
        """
        input_data = {}

        if search_text:
            input_data['search_text'] = search_text

        if start_id:
            input_data['start_id'] = start_id

        return await self.request(
            method='getMyArchivedStickerSets',
            input=input_data
        )