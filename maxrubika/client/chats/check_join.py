import maxrubika
from ..exceptions import InvalidInput

class CheckJoin:
    async def check_join(
        self: "maxrubika.Client",
        chat: str,
        member: str
    ) -> bool:
        """
        Check if a user or bot is a member of a specific group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the chat to check.
            member (str): The GUID or username of the user/bot to check.

        Returns:
            bool: True if user/bot is a member, False otherwise.
        """
        member_guid = await self.get_guid(member)
        if not member_guid.startswith(("u0", "b0")):
            message = f"'{member}' does not point to a valid member. Expected a user GUID, bot GUID or username."
            raise InvalidInput(message)

        chat_guid = await self.get_guid(chat)
        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        is_bot = member_guid.startswith("b0")
        is_group = chat_guid.startswith("g0")
        is_channel = chat_guid.startswith("c0")

        if is_group:
            if is_bot:
                bot_info = await self.get_chat_info(member_guid)

                username = None
                if isinstance(bot_info, dict):
                    username = bot_info.get('bot', {}).get('username')
                elif hasattr(bot_info, 'bot'):
                    username = getattr(bot_info.bot, 'username', None)

                if username:
                    result = await self.get_group_members(chat_guid, search_text=username)
                else:
                    result = await self.get_group_members(chat_guid)

                members = []
                if isinstance(result, dict):
                    members = result.get('in_chat_members', [])
                elif hasattr(result, 'in_chat_members'):
                    members = result.in_chat_members

                for memberx in members:
                    a_member_guid = memberx.get('member_guid') if isinstance(memberx, dict) else memberx.member_guid
                    if a_member_guid == member_guid:
                        return True
                return False

            else:
                common_result = await self.get_common_groups(member_guid)

                groups = []
                if isinstance(common_result, dict):
                    groups = common_result.get('abs_groups', [])
                elif hasattr(common_result, 'abs_groups'):
                    groups = common_result.abs_groups

                for group in groups:
                    g_guid = group.get('object_guid') if isinstance(group, dict) else group.object_guid
                    if g_guid == chat_guid:
                        return True
                return False

        if is_channel:
            info = await self.get_chat_info(member_guid)

            username = None
            if is_bot:
                if isinstance(info, dict):
                    username = info.get('bot', {}).get('username')
                elif hasattr(info, 'bot'):
                    username = getattr(info.bot, 'username', None)
            else:
                if isinstance(info, dict):
                    username = info.get('user', {}).get('username')
                elif hasattr(info, 'user'):
                    username = getattr(info.user, 'username', None)

            if username:
                result = await self.get_channel_members(chat_guid, search_text=username)
            else:
                result = await self.get_channel_members(chat_guid)

            members = []
            if isinstance(result, dict):
                members = result.get('in_chat_members', [])
            elif hasattr(result, 'in_chat_members'):
                members = result.in_chat_members

            for memberx in members:
                a_member_guid = memberx.get('member_guid') if isinstance(memberx, dict) else memberx.member_guid
                if a_member_guid == member_guid:
                    return True
            return False

        return False