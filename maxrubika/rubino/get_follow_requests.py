from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetFollowRequests:
    async def get_follow_requests(
        self: "maxrubika.Rubino",
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get pending follow requests.

        Parameters:
            start_id (str, optional): The starting event ID for pagination. Defaults to None.
            my_profile (str, optional): The profile to query. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        return await self.get_events(
            filter='FollowRequest',
            start_id=start_id,
            my_profile=my_profile
        )