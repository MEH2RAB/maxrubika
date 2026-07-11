import maxrubika

class GetAvailableReactions:
    async def get_available_reactions(self: "maxrubika.Client"):
        """
        Retrieve the list of available message reactions that can be used in chats.

        Returns:
            Shows available reactions data from the server.
        """
        return await self.request(method = 'getAvailableReactions')