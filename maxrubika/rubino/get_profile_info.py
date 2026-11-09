from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetProfileInfo:
    async def get_profile_info(
        self: "maxrubika.Rubino",
        target_profile: str,
        my_profile: Optional[str] = None
    ):
        """
        Get detailed profile information.

        Parameters:
            target_profile (str): The profile ID or username.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The profile information data.
        """
        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'target_profile_id': target_profile_id
        }

        return await self.request(
            method='getProfileInfo',
            input=input_data
        )