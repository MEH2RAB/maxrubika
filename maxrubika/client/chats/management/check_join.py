from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CheckJoin:
    async def check_join(
        self: "maxrubika.Messenger",
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
        from ....data import Data
        from ...exceptions import InvalidInput

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
                if isinstance(bot_info, dict):
                    bot_info = Data(bot_info)
                username = bot_info.find_keys('username')

                if username:
                    result = await self.get_group_members(chat_guid, search_text=username)
                else:
                    result = await self.get_group_members(chat_guid)

                if isinstance(result, dict):
                    result = Data(result)

                members = result.find_keys('in_chat_members') or []

                for memberx in members:
                    if isinstance(memberx, dict):
                        memberx = Data(memberx)
                    a_member_guid = memberx.find_keys('member_guid')
                    if a_member_guid == member_guid:
                        return True
                return False

            else:
                common_result = await self.get_common_groups(member_guid)

                if isinstance(common_result, dict):
                    common_result = Data(common_result)

                groups = common_result.find_keys('abs_groups') or []

                for group in groups:
                    if isinstance(group, dict):
                        group = Data(group)
                    g_guid = group.find_keys('object_guid')
                    if g_guid == chat_guid:
                        return True
                return False

        if is_channel:
            info = await self.get_chat_info(member_guid)

            if isinstance(info, dict):
                info = Data(info)

            username = info.find_keys('username')

            if username:
                result = await self.get_channel_members(chat_guid, search_text=username)
            else:
                result = await self.get_channel_members(chat_guid)

            if isinstance(result, dict):
                result = Data(result)

            members = result.find_keys('in_chat_members') or []

            for memberx in members:
                if isinstance(memberx, dict):
                    memberx = Data(memberx)
                a_member_guid = memberx.find_keys('member_guid')
                if a_member_guid == member_guid:
                    return True
            return False

        return False