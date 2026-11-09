from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPlaySuggestedEpisode:
    async def get_play_suggested_episode(
        self: "maxrubika.RubikaTV",
        series_id: str,
        track_id: Optional[str] = None
    ):
        """
        Retrieve the suggested next episode for a series.

        Parameters:
            series_id (str): Identifier of the series.
            track_id (str, optional): Optional tracking identifier (session hash string).

        Returns:
            The API output.
        """
        input_data = {"series_id": series_id}

        if track_id is not None:
            input_data["track_id"] = track_id

        return await self.request(
            method="getPlaySuggestedEpisode",
            input=input_data
        )