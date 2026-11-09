from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetCallSignalingData:
    async def get_call_signaling_data(
        self: "maxrubika.Messenger",
        call_id: str
    ):
        """
        Get signaling data for a call (needed for WebRTC connection).

        Parameters:
            call_id (str): The ID of the call.

        Returns:
            The result of the API call, containing signaling data.
        """
        return await self.request(
            method='getSignalingData',
            input={'call_id': call_id}
        )