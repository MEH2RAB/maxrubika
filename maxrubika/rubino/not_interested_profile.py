from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class NotInterestedProfile:
    async def not_interested_profile(
        self: "maxrubika.Rubino",
        target_profile: str,
        track_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Mark a profile as "not interested".

        Parameters:
            target_profile (str): The profile ID or username to mark as not interested.
            track_id (str, optional): A tracking ID. Defaults to None.
            my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

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
            'target_profile_id': target_profile_id,
            'action': 'NotInterested'
        }

        if track_id is not None:
            input_data['track_id'] = track_id

        return await self.request(
            method='setProfileFeedback',
            input=input_data
        )