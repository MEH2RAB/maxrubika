from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPostLikes:
    async def get_post_likes(
        self: "maxrubika.Rubino",
        target_profile: str,
        post_id: str,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get the list of users who liked a post.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post_id (str): The ID of the post.
            start_id (str, optional): The starting user ID for pagination. Defaults to None.
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
            'post_profile_id': target_profile_id,
            'post_id': post_id
        }

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getPostLikes',
            input=input_data
        )