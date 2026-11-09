from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ReportComment:
    async def report_comment(
        self: "maxrubika.Rubino",
        target_profile: str,
        post: str,
        comment_id: str,
        reason: int = 2,
        my_profile: Optional[str] = None
    ):
        """
        Report a comment.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post (str): The post link or post ID that contains the comment.
            comment_id (str): The ID of the comment.
            reason (int): Report reason code. Defaults to 2.
            my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        post_id = await self.get_post_id(post, my_profile=my_profile)
        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'record_key': comment_id,
            'post_profile_id': target_profile_id,
            'comment_post_id': post_id,
            'reason': reason,
            'model': 'Comment'
        }

        return await self.request(
            method='reportRecord',
            input=input_data
        )