from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnsetProfileAdmin:
    async def unset_profile_admin(
        self: "maxrubika.Rubino",
        target_profile: str,
        my_profile: Optional[str] = None
    ):
        """
        Unset (remove) all admin access for a profile.

        Parameters:
            target_profile (str): The profile ID or username of the admin.
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
            'action': 'Unset',
            'access_list': []
        }

        return await self.request(
            method='setProfileAdmin',
            input=input_data
        )