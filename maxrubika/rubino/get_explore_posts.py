from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetExplorePosts:
    async def get_explore_posts(
        self: "maxrubika.Rubino",
        topic_id: Optional[str] = None,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get posts from the Explore feed.

        Parameters:
            topic_id (str, optional): The topic ID to filter posts by. Defaults to None (all topics).
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

        if topic_id is not None:
            input_data['topic_id'] = topic_id

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getExplorePosts',
            input=input_data
        )