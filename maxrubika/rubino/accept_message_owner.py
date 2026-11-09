from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AcceptMessageOwner:
    async def accept_message_owner(
        self: "maxrubika.Rubino",
        target_profile: str,
        my_profile: Optional[str] = None
    ):
        """
        Accept a message request from a profile.

        Parameters:
            target_profile (str): The profile ID or username that sent the message request.
            my_profile (str, optional): The profile that accepts. Defaults to self.profile_id.

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
            method='settingMessageOwnerAction',
            input=input_data
        )