import maxrubika
from .exceptions import InvalidAccess

class MemberIsJoined:
    async def member_is_joined(
        self: "maxrubika.Bot",
        chat_id: str,
        user_id: str
    ) -> bool:
        """
        Check whether a user is a member of the given chat.

        Parameters:
            chat_id (str): chat_id of group (g0...) or channel (c0...).
            user_id (str): user_id of the user (u0...).

        Returns:
            bool: True if the user is a member, else False.
        """
        try:
            await self.get_chat_member(chat_id, user_id)
            return True
        except InvalidAccess:
            return False