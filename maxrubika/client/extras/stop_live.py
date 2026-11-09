from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class StopLive:
    async def stop_live(
        self: "maxrubika.Messenger",
        live_id: str
    ):
        """
        Stop a live stream.

        Parameters:
            live_id (str): Live stream ID.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='stopLive',
            input={'live_id': live_id}
        )