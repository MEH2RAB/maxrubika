from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class TerminateOtherSessions:
    async def terminate_other_sessions(self: "maxrubika.Messenger"):
        """
        Terminate other account sessions.

        Returns:
            The result of the API call.
        """
        return await self.request(method='terminateOtherSessions')