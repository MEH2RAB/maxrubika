from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetBoostUrl:
    async def get_boost_url(
        self: "maxrubika.Rubino",
        target_profile: str,
        post_id: str,
        my_profile: Optional[str] = None
    ):
        """
        Get the boost URL for a post.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post_id (str): The ID of the post to boost.
            my_profile (str, optional): The profile that performs the boost. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        target_profile_id = await self.get_profile_id(target_profile)

        input_data = {
            'profile_id': profile_id,
            'object_id': post_id,
            'post_profile_id': target_profile_id,
            'type': 'Post'
        }

        return await self.request(
            method='getBoostUrl',
            input=input_data
        )