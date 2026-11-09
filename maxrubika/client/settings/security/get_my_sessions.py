from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMySessions:
    async def get_my_sessions(self: "maxrubika.Messenger"):
        """
        Get information about the current user's sessions.

        Returns:
            Information about the user's sessions.
        """
        return await self.request(method='getMySessions')