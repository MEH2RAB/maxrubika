from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMyProfileSettings:
    async def get_my_profile_settings(
        self: "maxrubika.Rubino",
        my_profile: Optional[str] = None
    ):
        """
        Get the settings of a profile.

        Parameters:
            my_profile (str, optional): The profile to query. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        return await self.request(
            method='getProfileSetting',
            input={'profile_id': profile_id}
        )