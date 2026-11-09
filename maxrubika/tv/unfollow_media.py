from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnFollowMedia:
    async def unfollow_media(
        self: "maxrubika.RubikaTV",
        media_id: str,
        track_id: Optional[str] = None
    ):
        """
        Unfollow a media.

        Parameters:
            media_id (str): Identifier of the media.
            track_id (str, optional): Optional tracking identifier.

        Returns:
            The API output.
        """
        input_data = {
            "action": "UnFollow",
            "media_id": media_id
        }

        if track_id is not None:
            input_data["track_id"] = track_id

        return await self.request(
            method="actionOnMedia",
            input=input_data
        )