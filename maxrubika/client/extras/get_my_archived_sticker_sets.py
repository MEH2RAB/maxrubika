import maxrubika

class GetMyArchivedStickerSets:
    async def get_my_archived_sticker_sets(
        self: "maxrubika.Client",
        start_id: str = None
    ):
        """
        Get archived sticker sets of the current user.

        Parameters:
            start_id (str, optional): The ID to start fetching from. Defaults to None.

        Returns:
            The result of the API call.
        """
        input = {}
        if start_id:
            input['start_id'] = start_id

        return await self.request(
            method = 'getMyArchivedStickerSets',
            input = input
        )