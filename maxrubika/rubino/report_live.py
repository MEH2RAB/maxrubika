from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ReportLive:
    async def report_live(
        self: "maxrubika.Rubino",
        target_profile: str,
        live_id: str,
        reason: int = 2,
        my_profile: Optional[str] = None
    ):
        """
        Report a live stream.

        Parameters:
            target_profile (str): The profile ID or username that owns the live.
            live_id (str): The ID of the live stream to report.
            reason (int): Report reason code. Defaults to 2.
            my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'record_key': live_id,
            'live_profile_id': target_profile_id,
            'reason': reason,
            'model': 'Live'
        }

        return await self.request(
            method='reportRecord',
            input=input_data
        )