from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class TerminateSession:
    async def terminate_session(self: "maxrubika.Messenger", session_key: str):
        """
        Terminate a user session.

        Parameters:
            session_key (str): The session key of the session to be terminated.

        Returns:
            The result of the API call.
        """
        return await self.request(method='terminateSession', input={'session_key': session_key})