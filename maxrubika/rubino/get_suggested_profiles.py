from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetSuggestedProfiles:
    async def get_suggested_profiles(
        self: "maxrubika.Rubino",
        target_profile: str,
        usage: str = 'Similar',
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get suggested profiles.

        Parameters:
            target_profile (str): The reference profile ID or username for similarity.
            usage (str, optional): The suggestion usage type. Default is 'Similar'.
            start_id (str, optional): The starting profile ID for pagination. Defaults to None.
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
            'usage': usage,
            'usage_data': {'target_profile_id': target_profile_id}
        }

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getSuggestedProfiles',
            input=input_data
        )