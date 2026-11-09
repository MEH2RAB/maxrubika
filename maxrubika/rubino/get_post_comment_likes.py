from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPostCommentLikes:
    async def get_post_comment_likes(
        self: "maxrubika.Rubino",
        post: str,
        comment_id: str,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get the list of users who liked a post comment.

        Parameters:
            post (str): The post link or post ID.
            comment_id (str): The ID of the comment.
            start_id (str, optional): The starting user ID for pagination. Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        post_id = await self.get_post_id(post, my_profile=my_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'post_id': post_id,
            'comment_id': comment_id
        }

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getPostCommentLikes',
            input=input_data
        )