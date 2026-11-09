from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPostLink:
    async def get_post_link(
        self: "maxrubika.Rubino",
        target_profile: str,
        post_id: str,
        my_profile: Optional[str] = None
    ):
        """
        Get the share link of a post.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post_id (str): The ID of the post.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

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
            'post_id': post_id,
            'post_profile_id': target_profile_id
        }

        return await self.request(
            method='getShareLink',
            input=input_data
        )