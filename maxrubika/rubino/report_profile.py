from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ReportProfile:
    async def report_profile(
        self: "maxrubika.Rubino",
        target_profile: str,
        reason: int = 2,
        my_profile: Optional[str] = None
    ):
        """
        Report a profile.

        Parameters:
            target_profile (str): The profile ID or username to report.
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

        if self.api_version == 1:
            input_data = {
                'profile_id': profile_id,
                'record_key': target_profile_id,
                'reason': reason,
                'model': 'Profile'
            }
            method = 'reportRecord'
        else:
            input_data = {
                'profile_id': profile_id,
                'model': 'Profile',
                'record_id': target_profile_id,
                'reason': reason
            }
            method = 'setReportRecord'

        return await self.request(
            method=method,
            input=input_data
        )