from typing import Literal
import maxrubika
from ..exceptions import InvalidInput

class SetAskSpam:
    async def set_ask_spam(
        self: "maxrubika.Client",
        chat: str,
        action: Literal['AddToContact', 'BlockUser', 'Cancel', 'ReportAndLeave'] = 'Cancel'
    ):
        """
        Perform an action for a pending spam request.

        Parameters:
            chat (str): The GUID, link, or username of the user, group, or channel.
            action (str): The action to apply:
                - For user: 'AddToContact', 'BlockUser', 'Cancel'.
                - For group/channel: 'ReportAndLeave'.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        is_user = chat_guid.startswith("u0")
        is_group_channel = chat_guid.startswith(("g0", "c0"))

        if not is_user and not is_group_channel:
            message = f"'{chat}' does not point to a valid chat. Expected a user GUID/username, group link, or channel link."
            raise InvalidInput(message)

        action = action.lower()
        if is_user:
            if action == "addtocontact":
                action = "AddToContact"
            elif action == "blockuser":
                action = "BlockUser"
            elif action == "cancel":
                action = "Cancel"
            else:
                raise InvalidInput(
                    f"Invalid action for user: '{action}'. Expected 'AddToContact', 'BlockUser', or 'Cancel'."
                )
        elif is_group_channel:
            if action == "reportandleave":
                action = "ReportAndLeave"
            elif action == "cancel":
                action = "Cancel"
            else:
                raise InvalidInput(
                    f"Invalid action for group/channel: '{action}'. Expected 'ReportAndLeave' or 'Cancel'."
                )

        return await self.request(
            method = 'setAskSpamAction',
            input = {'object_guid': chat_guid, 'action': action}
        )