import maxrubika

class TerminateOtherSessions:
    async def terminate_other_sessions(self: "maxrubika.Client"):
        """
        Terminate other account sessions.

        Returns:
            The result of the API call.
        """
        return await self.request(method = 'terminateOtherSessions')