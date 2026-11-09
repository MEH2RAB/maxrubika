from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMedia:
    async def get_media(
        self: "maxrubika.RubikaTV",
        media_id: str,
        track_id: Optional[str] = None
    ):
        """
        Retrieve media details by its ID.

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
            method="getMedia",
            input=input_data
        )