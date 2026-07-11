import re
import maxrubika
from ..exceptions import (
    InvalidGroupLink,
    InvalidChannelLink, 
    InvalidUsername,
    InvalidChatInput,
    InvalidInput
)

class GetGuid:
    async def get_guid(self: "maxrubika.Client", chat: str) -> str:
        """
        Retrieves the GUID of a user, group, channel, or bot.

        Parameters:
            chat (str): The username, group link, channel link, or bot username.

        Returns:
            str: The GUID of the chat.
        """
        if not isinstance(chat, str):
            raise InvalidInput(
                f"Invalid chat input: '{chat}' is type {type(chat).__name__}, expected str"
            )

        if not chat or not chat.strip():
            raise InvalidInput(
                "Chat input cannot be empty. Please provide a valid chat GUID, link, or username."
            )

        chat = chat.strip()
        chat_lower = chat.lower()

        if chat_lower.startswith("https://rubika.ir/joing"):
            result = await self.get_info_by_link(chat)
            info = result.to_dict() if hasattr(result, 'to_dict') else result
            if not info.get("is_valid"):
                raise InvalidGroupLink()
            return info["group"]["group_guid"]

        if chat_lower.startswith("https://rubika.ir/joinc"):
            result = await self.get_info_by_link(chat)
            info = result.to_dict() if hasattr(result, 'to_dict') else result
            if not info.get("is_valid"):
                raise InvalidChannelLink()
            return info["channel"]["channel_guid"]

        if re.match(r"^([cubsg]0)[a-zA-Z0-9]{30}$", chat):
            return chat

        result = await self.get_info_by_username(chat)
        info = result.to_dict() if hasattr(result, 'to_dict') else result

        if not info.get("exist"):
            raise InvalidUsername()
        chat_type = info.get("type")
        if chat_type == "User":
            return info["user"]["user_guid"]
        if chat_type == "Bot":
            return info["bot"]["bot_guid"]
        if chat_type == "Channel":
            return info["channel"]["channel_guid"]
        raise InvalidChatInput()