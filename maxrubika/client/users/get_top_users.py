import maxrubika

class GetTopUsers:
    """
    Get top users list methods.
    """
    async def get_top_users(self: "maxrubika.Client"):
        """
        Get list of top users.

        Returns:
            List of top users.
        """
        return await self.request(method = 'getTopChatUsers')