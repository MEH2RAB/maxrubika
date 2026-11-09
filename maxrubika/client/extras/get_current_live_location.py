from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetCurrentLiveLocation:
    async def get_current_live_location(
        self: "maxrubika.Messenger",
        live_loc_track_id: str
    ):
        """
        Get the current live location by its track ID.

        Parameters:
            live_loc_track_id (str): The live location track ID.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='getCurrentLiveLocation',
            input={'live_loc_track_id': live_loc_track_id}
        )