from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetExplorePostTopics:
    async def get_explore_post_topics(
        self: "maxrubika.Rubino",
        my_profile: Optional[str] = None
    ):
        """
        Get explore post topics.

        Parameters:
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The topics data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        return await self.request(
            method='getExplorePostTopics',
            input={'profile_id': profile_id}
        )