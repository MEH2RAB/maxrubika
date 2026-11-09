from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChatInfo:
    async def get_chat_info(
        self: "maxrubika.Messenger",
        chat: str
    ):
        """
        Get information about a user, group, or channel.

        Parameters:
            chat (str): The GUID, link, or username of the chat (user, group, or channel).

        Returns:
            The update containing information about the chat.
        """
        import re
        from ....data import Data
        from ...exceptions import InvalidAccess

        if re.match(r"^([cubsg]0)[a-zA-Z0-9]{30}$", chat):
            first_char = chat[0]
            if first_char == "u":
                return await self.get_user_info(chat)
            elif first_char == "b":
                return await self.get_bot_info(chat)
            elif first_char == "c":
                return await self.get_channel_info(chat)
            elif first_char == "g":
                return await self.get_group_info(chat)
            elif first_char == "s":
                return await self.get_service_info(chat)

        if "joing" in chat:
            info_chat = await self.get_info_by_link(chat)

            if isinstance(info_chat, dict):
                info_chat = Data(info_chat)

            is_valid = info_chat.find_keys('is_valid')
            group_guid = info_chat.find_keys('group_guid')

            if is_valid and group_guid:
                try:
                    return await self.get_group_info(group_guid)
                except InvalidAccess:
                    return info_chat

            return info_chat

        if "joinc" in chat:
            info_chat = await self.get_info_by_link(chat)

            if isinstance(info_chat, dict):
                info_chat = Data(info_chat)

            is_valid = info_chat.find_keys('is_valid')
            channel_guid = info_chat.find_keys('channel_guid')

            if is_valid and channel_guid:
                try:
                    return await self.get_channel_info(channel_guid)
                except InvalidAccess:
                    return info_chat

            return info_chat

        info_chat = await self.get_info_by_username(chat)

        if isinstance(info_chat, dict):
            info_chat = Data(info_chat)

        exist = info_chat.find_keys('exist')

        if exist:
            obj_type = info_chat.find_keys('type')

            if obj_type == "User":
                user_guid = info_chat.find_keys('user_guid')
                return await self.get_user_info(user_guid)

            elif obj_type == "Bot":
                bot_guid = info_chat.find_keys('bot_guid')
                return await self.get_bot_info(bot_guid)

            elif obj_type == "Channel":
                channel_guid = info_chat.find_keys('channel_guid')
                return await self.get_channel_info(channel_guid)

        return info_chat