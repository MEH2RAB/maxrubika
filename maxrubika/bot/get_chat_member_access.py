from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChatMemberAccess:
    async def get_chat_member_access(
        self: "maxrubika.Bot",
        chat_id: str,
        user_id: str
    ):
        """
        Get the access list of a specific member in a chat.

        Parameters:
            chat_id (str): chat_id of group (g0...), channel (c0...), or bot (b0...).
            user_id (str): user_id of the user (u0...).

        Returns:
            list: The list of access permissions for the member.
        """
        from ..data import Data

        member = await self.get_chat_member(chat_id, user_id)

        if isinstance(member, dict):
            member = Data(member)

        access_list = member.find_keys('access_list')

        return list(access_list)