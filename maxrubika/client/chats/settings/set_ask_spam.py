from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetAskSpam:
    USER_ACTIONS = {
        'addtocontact': 'AddToContact',
        'blockuser': 'BlockUser',
        'cancel': 'Cancel'
    }

    GROUP_CHANNEL_ACTIONS = {
        'reportandleave': 'ReportAndLeave'
    }

    async def set_ask_spam(
        self: "maxrubika.Messenger",
        chat: str,
        action: Literal['AddToContact', 'BlockUser', 'Cancel', 'ReportAndLeave'] = 'Cancel'
    ):
        """
        Perform an action for a pending spam request.

        Parameters:
            chat (str): The GUID, link, or username of the user, group, or channel.
            action (str): The action to apply. Case-insensitive. For user (u0): 'AddToContact', 'BlockUser', 'Cancel'. For group/channel (g0/c0): 'ReportAndLeave'.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        is_user = chat_guid.startswith("u0")
        is_group_channel = chat_guid.startswith(("g0", "c0"))

        if not is_user and not is_group_channel:
            message = f"'{chat}' does not point to a valid chat. Expected a user GUID/username, group link, or channel link."
            raise InvalidInput(message)

        action_lower = str(action).lower()

        if is_user:
            normalized_action = self.USER_ACTIONS.get(action_lower)
            if not normalized_action:
                message = f"Invalid action for user: '{action}'. Expected 'AddToContact', 'BlockUser', or 'Cancel'."
                raise InvalidInput(message)
        else:
            normalized_action = self.GROUP_CHANNEL_ACTIONS.get(action_lower)
            if not normalized_action:
                message = f"Invalid action for group/channel: '{action}'. Expected 'ReportAndLeave'."
                raise InvalidInput(message)

        input_data = {'object_guid': chat_guid, 'action': normalized_action}

        return await self.request(method='setAskSpamAction', input=input_data)