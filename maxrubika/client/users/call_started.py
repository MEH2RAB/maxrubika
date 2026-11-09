from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CallStarted:
    async def call_started(
        self: "maxrubika.Messenger",
        call_id: str
    ):
        """
        Notify the server that a call has started.

        Parameters:
            call_id (str): The ID of the call that has started.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='callStarted',
            input={'call_id': call_id}
        )