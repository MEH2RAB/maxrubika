from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetLiveReport:
    async def get_live_report(
        self: "maxrubika.Messenger",
        live_id: str
    ):
        """
        Get the report and statistics of a completed live stream.

        Parameters:
            live_id (str): The ID of the live stream.

        Returns:
            The result of the API call, containing live stats and graphs.
        """
        return await self.request(
            method='getLiveReport',
            input={'live_id': live_id}
        )