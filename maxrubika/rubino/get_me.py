from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMe:
    async def get_me(
        self: "maxrubika.Rubino",
        my_profile: Optional[str] = None
    ):
        """
        Get profile information.

        Parameters:
            my_profile (str, optional): The profile ID or username.
                Defaults to self.profile_id.

        Returns:
            The profile data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {}
        if profile_id:
            input_data['profile_id'] = profile_id

        method = 'getMyProfileList' if self.api_version == 1 else 'getProfileList'

        return await self.request(
            method=method,
            input=input_data
        )