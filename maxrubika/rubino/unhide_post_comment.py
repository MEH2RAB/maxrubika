from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnhidePostComment:
    async def unhide_post_comment(
        self: "maxrubika.Rubino",
        post: str,
        comment_id: str,
        post_track_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Unhide a comment on a post.

        Parameters:
            post (str): The post link or post ID.
            comment_id (str): The ID of the comment.
            post_track_id (str, optional): The post track ID. Defaults to None.
            my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

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
            'comment_id': comment_id,
            'action': 'Unhide'
        }

        if post_track_id is not None:
            input_data['post_track_id'] = post_track_id

        return await self.request(
            method='postCommentAction',
            input=input_data
        )