from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetSavedPosts:
    async def get_saved_posts(
        self: "maxrubika.Rubino",
        start_id: Optional[str] = None,
        bookmark_collection_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get the list of bookmarked (saved) posts.

        Parameters:
            start_id (str, optional): The starting post ID for pagination. Defaults to None.
            bookmark_collection_id (str, optional): The bookmark collection ID to filter by. Defaults to None.
            my_profile (str, optional): The profile to query. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {'profile_id': profile_id}

        if start_id is not None:
            input_data['start_id'] = start_id

        if bookmark_collection_id is not None:
            input_data['bookmark_collection_id'] = bookmark_collection_id

        return await self.request(
            method='getBookmarkedPosts',
            input=input_data
        )