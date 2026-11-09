from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetNextMediaInfo:
    async def get_next_media_info(
        self: "maxrubika.RubikaTV",
        media_id: str,
        track_id: Optional[str] = None
    ):
        """
        Retrieve the next media info after the given media.

        Parameters:
            media_id (str): Identifier of the media.
            track_id (str, optional): Optional tracking identifier (session hash string).

        Returns:
            The API output.
        """

        input_data = {"media_id": media_id}

        if track_id is not None:
            input_data["track_id"] = track_id

        return await self.request(
            method="getNextMediaInfo",
            input=input_data
        )