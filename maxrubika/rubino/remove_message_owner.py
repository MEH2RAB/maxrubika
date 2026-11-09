from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RemoveMessageOwner:
    async def remove_message_owner(
        self: "maxrubika.Rubino",
        target_profile: str,
        my_profile: Optional[str] = None
    ):
        """
        Remove message access for a profile.

        Parameters:
            target_profile (str): The profile ID or username whose message access will be removed.
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
            'action': 'Remove'
        }

        return await self.request(
            method='settingMessageOwnerAction',
            input=input_data
        )