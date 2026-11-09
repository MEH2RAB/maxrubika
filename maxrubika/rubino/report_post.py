from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ReportPost:
    async def report_post(
        self: "maxrubika.Rubino",
        target_profile: str,
        post: str,
        reason: int = 2,
        my_profile: Optional[str] = None
    ):
        """
        Report a post.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post (str): The post link or post ID.
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

        if self.api_version == 1:
            input_data = {
                'profile_id': profile_id,
                'record_key': post_id,
                'post_profile_id': target_profile_id,
                'reason': reason,
                'model': 'Post'
            }
            method = 'reportRecord'
        else:
            input_data = {
                'profile_id': profile_id,
                'model': 'Post',
                'record_id': post_id,
                'post_profile_id': target_profile_id,
                'reason': reason
            }
            method = 'setReportRecord'

        return await self.request(
            method=method,
            input=input_data
        )