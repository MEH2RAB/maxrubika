from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class StopLiveLocation:
    async def stop_live_location(
        self: "maxrubika.Messenger",
        live_loc_track_id: str
    ):
        """
        Stop a live location by its track ID.

        Parameters:
            live_loc_track_id (str): The live location track ID.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='stopLiveLocation',
            input={'live_loc_track_id': live_loc_track_id}
        )