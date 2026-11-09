from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AcceptProfileAdmin:
    async def accept_profile_admin(
        self: "maxrubika.Rubino",
        target_profile: str,
        my_profile: Optional[str] = None
    ):
        """
        Accept a profile admin invitation.

        Parameters:
            target_profile (str): The profile ID or username of the page that sent the admin invitation.
            my_profile (str, optional): The profile that accepts the invitation. Defaults to self.profile_id.

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
            'action': 'Accept'
        }

        return await self.request(
            method='profileAdminAction',
            input=input_data
        )