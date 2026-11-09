from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ReceivedCall:
    async def received_call(
        self: "maxrubika.Messenger",
        call_id: str
    ):
        """
        Notify the server that an incoming call has been received.

        Parameters:
            call_id (str): The ID of the received call.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='receivedCall',
            input={'call_id': call_id}
        )