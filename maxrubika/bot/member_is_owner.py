from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class MemberIsOwner:
    async def member_is_owner(
        self: "maxrubika.Bot",
        chat_id: str,
        user_id: str
    ) -> bool:
        """
        Check whether a member is the owner of the given chat.

        Parameters:
            chat_id (str): chat_id of group (g0...) or channel (c0...).
            user_id (str): user_id of the member (u0...).

        Returns:
            bool: True if status is 'Creator', else False.
        """
        from ..data import Data

        result = await self.get_chat_member(chat_id, user_id)

        if isinstance(result, dict):
            result = Data(result)

        data = result.find_keys('data')
        chat_member = data.find_keys('chat_member')
        status = chat_member.find_keys('status') if chat_member else None

        return status == "Creator"