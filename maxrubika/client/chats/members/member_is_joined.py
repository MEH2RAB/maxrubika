from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class MemberIsJoined:
    async def member_is_joined(
        self: "maxrubika.Messenger",
        chat: str,
        member: str
    ) -> bool:
        """
        Check if a user or bot is a member of a specific group or channel.

        Alias for `check_join`.

        Parameters:
            chat (str): The GUID, link, or username of the chat to check.
            member (str): The GUID or username of the user/bot to check.

        Returns:
            bool: True if user/bot is a member, False otherwise.
        """
        return await self.check_join(chat, member)