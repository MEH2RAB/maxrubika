from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetTopUsers:
    async def get_top_users(self: "maxrubika.Messenger"):
        """
        Get list of top users.

        Returns:
            List of top users.
        """
        return await self.request(method='getTopChatUsers')