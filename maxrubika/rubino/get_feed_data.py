from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetFeedData:
    async def get_feed_data(
        self: "maxrubika.Rubino",
        limit: Optional[int] = None,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get feed posts.

        Parameters:
            limit (int, optional): The maximum number of posts to return. Defaults to None (server default).
            start_id (str, optional): The starting post ID for pagination. Defaults to None.
            my_profile (str, optional): The profile to query. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {'profile_id': profile_id}

        if limit is not None:
            input_data['limit'] = limit

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getFeedData',
            input=input_data
        )