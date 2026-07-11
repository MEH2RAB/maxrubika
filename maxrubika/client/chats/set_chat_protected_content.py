import maxrubika
from ..exceptions import InvalidInput

class SetChatProtectedContent:
    async def set_chat_protected_content(
        self: "maxrubika.Client",
        chat: str,
        enabled: bool
    ):
        """
        Set the chat protected content setting.

        Parameters:
            chat (int): The GUID or username of the target chat.
            enabled (bool): Pass True to enable the protected content setting, False to disable.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        if chat_guid.startswith('g0'):
            return await self.edit_group_info(group = chat_guid, is_restricted_content = enabled)

        else:
            return await self.edit_channel_info(channel = chat_guid, is_restricted_content = enabled)