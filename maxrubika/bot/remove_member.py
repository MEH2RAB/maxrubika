from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RemoveMember:
    async def remove_member(
        self: "maxrubika.Bot",
        chat_id: str,
        sender_id: str
    ):
        """
        Remove (ban) a member from a group or channel.

        Parameters:
            chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0').
            sender_id (str): sender_id of member to ban.

        Returns:
            The API response.
        """
        return await self.ban_member(chat_id, sender_id)