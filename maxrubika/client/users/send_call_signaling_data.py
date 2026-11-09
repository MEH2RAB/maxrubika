from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendCallSignalingData:
    async def send_call_signaling_data(
        self: "maxrubika.Messenger",
        call_id: str,
        data: str
    ):
        """
        Send signaling data for a call.

        Parameters:
            call_id (str): The ID of the call.
            data (str): Signaling data as a string (e.g., JSON-encoded SDP/ICE).

        Returns:
            The result of the API call.
        """
        input_data = {
            'call_id': call_id,
            'data': data
        }

        return await self.request(
            method='sendSignalingData',
            input=input_data
        )