from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CheckJoin:
    async def check_join(
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
        return await self.member_is_joined(chat_id, user_id)