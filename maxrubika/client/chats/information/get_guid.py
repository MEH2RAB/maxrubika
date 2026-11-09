from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetGuid:
    async def get_guid(self: "maxrubika.Messenger", chat: str) -> str:
        """
        Retrieves the GUID of a user, group, channel, or bot.

        Parameters:
            chat (str): The username, group link, channel link, or bot username.

        Returns:
            str: The GUID of the chat.
        """
        import re
        from ....data import Data
        from ...exceptions import (
            InvalidGroupLink,
            InvalidChannelLink,
            InvalidUsername,
            InvalidChatInput,
            InvalidInput
        )

        if not isinstance(chat, str):
            message = f"Invalid chat input: '{chat}' is type {type(chat).__name__}, expected str"
            raise InvalidInput(message)

        if not chat or not chat.strip():
            message = "Chat input cannot be empty. Please provide a valid chat GUID, link, or username."
            raise InvalidInput(message)

        chat = chat.strip()
        chat_lower = chat.lower()

        if chat_lower.startswith(("https://rubika.ir/joing/", "https://shad.ir/joing/")):
            result = await self.get_info_by_link(chat)
            if isinstance(result, dict):
                result = Data(result)
            if not result.find_keys("is_valid"):
                raise InvalidGroupLink()
            return result.find_keys("group_guid")

        if chat_lower.startswith(("https://rubika.ir/joinc/", "https://shad.ir/joinc/")):
            result = await self.get_info_by_link(chat)
            if isinstance(result, dict):
                result = Data(result)
            if not result.find_keys("is_valid"):
                raise InvalidChannelLink()
            return result.find_keys("channel_guid")

        if re.match(r"^([cubsg]0)[a-zA-Z0-9]{30}$", chat):
            return chat

        result = await self.get_info_by_username(chat)
        if isinstance(result, dict):
            result = Data(result)

        if not result.find_keys("exist"):
            raise InvalidUsername()

        chat_type = result.find_keys("type")

        if chat_type == "User":
            return result.find_keys("user_guid")
        if chat_type == "Bot":
            return result.find_keys("bot_guid")
        if chat_type == "Channel":
            return result.find_keys("channel_guid")

        raise InvalidChatInput()