from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetBlockedProfiles:
    async def get_blocked_profiles(
        self: "maxrubika.Rubino",
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get the list of blocked profiles.

        Parameters:
            start_id (str, optional): The starting profile ID for pagination. Defaults to None.
            my_profile (str, optional): The profile to query. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {'profile_id': profile_id}

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getBlockedProfiles',
            input=input_data
        )