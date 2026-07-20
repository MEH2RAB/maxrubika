import maxrubika

class GetUnconfirmedSessions:
    async def get_unconfirmed_sessions(self: "maxrubika.Client"):
        """
        Get a list of unconfirmed (pending) sessions for the current account.

        Returns:
            The result of the API call containing unconfirmed sessions.
        """
        return await self.request(method = 'getUnconfirmedSessions')