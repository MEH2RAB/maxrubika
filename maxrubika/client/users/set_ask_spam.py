from typing import Literal
import maxrubika
from ..exceptions import InvalidInput

class SetAskSpam:
    async def set_ask_spam(
        self: "maxrubika.Client",
        user: str,
        action: Literal['AddToContact', 'BlockUser'] = 'AddToContact'
    ):
        """
        Perform an action for a pending spam request.

        Parameters:
            user (str): The user GUID or username.
            action (str): The action to apply `'AddToContact' or 'BlockUser'`.

        Returns:
            The result of the API call.
        """
        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        if action.lower() == "addtocontact":
            action = "AddToContact"
        elif action.lower() == "blockuser":
            action = "BlockUser"
        else:
            raise InvalidInput(
                f"Invalid action: '{action}'. Expected 'AddToContact' or 'BlockUser'."
            )
        return await self.request(
            method = 'setAskSpamAction',
            input = {'object_guid': user_guid, 'action': action}
        )