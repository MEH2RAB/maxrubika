import maxrubika

class GetMySessions:
    async def get_my_sessions(self: "maxrubika.Client"):
        """
        Get information about the current user's sessions.

        Returns:
            Information about the user's sessions.
        """
        return await self.request(method = 'getMySessions')