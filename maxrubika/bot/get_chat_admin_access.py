from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChatAdminAccess:
    async def get_chat_admin_access(
        self: "maxrubika.Bot",
        chat_id: str,
        user_id: str
    ):
        """
        Get the access list of a specific admin in a chat.

        Parameters:
            chat_id (str): chat_id of group (g0...) or channel (c0...).
            user_id (str): user_id of the admin (u0...).

        Returns:
            list: The list of access permissions for the admin.
        """
        from ..data import Data
        from .exceptions import InvalidInput

        member = await self.get_chat_member(chat_id, user_id)

        if isinstance(member, dict):
            member = Data(member)

        status = member.data.find_keys('status')

        if status not in ('Admin', 'Creator'):
            message = f"User '{user_id}' is not an admin."
            raise InvalidInput(message)

        access_list = member.find_keys('access_list')

        return list(access_list)