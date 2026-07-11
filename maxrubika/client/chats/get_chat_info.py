import re
import maxrubika

class GetChatInfo:
    async def get_chat_info(
            self: "maxrubika.Client",
            chat: str
        ):
        """
        Get information about a user, group, or channel.

        Parameters:
            chat (str): The GUID or link or username of the chat (user, group, or channel).

        Returns:
            The update containing information about the chat.
        """
        if re.match(r"^([cubsg]0)[a-zA-Z0-9]{30}$", chat):
            match chat[0]:
                case "u": return await self.get_user_info(chat)
                case "b": return await self.get_bot_info(chat)
                case "c": return await self.get_channel_info(chat)
                case "g": return await self.get_group_info(chat)
                case "s": return await self.get_service_info(chat)

        if "joing" in chat:
            info_chat = await self.get_info_by_link(chat)
            if getattr(info_chat, 'is_valid', False) and hasattr(info_chat, 'group'):
                group_guid = info_chat.group.group_guid
                if group_guid:
                    try:
                        return await self.get_group_info(group_guid)
                    except Exception as e:
                        if "INVALID_ACCESS" in str(e):
                            return info_chat
                        raise
            return info_chat

        if "joinc" in chat:
            info_chat = await self.get_info_by_link(chat)
            if getattr(info_chat, 'is_valid', False) and hasattr(info_chat, 'channel'):
                channel_guid = info_chat.channel.channel_guid
                if channel_guid:
                    try:
                        return await self.get_channel_info(channel_guid)
                    except Exception as e:
                        if "INVALID_ACCESS" in str(e):
                            return info_chat
                        raise
            return info_chat

        info_chat = await self.get_info_by_username(chat)
        if hasattr(info_chat, 'exist') and info_chat.exist:
            obj_type = getattr(info_chat, 'type', None)
            match obj_type:
                case "User": return await self.get_user_info(info_chat.user.user_guid)
                case "Bot": return await self.get_bot_info(info_chat.bot.bot_guid)
                case "Channel": return await self.get_channel_info(info_chat.channel.channel_guid)
        return info_chat