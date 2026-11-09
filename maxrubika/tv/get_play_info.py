from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPlayInfo:
    async def get_play_info(
        self: "maxrubika.RubikaTV",
        media_id: str,
        type: Literal["Main", "Trailer"] = "Trailer",
        version: int = 1,
        track_id: Optional[str] = None
    ):
        """
        Retrieve playback information for a specific media.

        Parameters:
            media_id (str): Identifier of the media.
            type (str): Type of content ("Main" or "Trailer"). Case-insensitive.
            version (int): Version number.
            track_id (str, optional): Optional tracking identifier (session hash string).

        Returns:
            The API output.
        """
        from .exceptions import InvalidInput

        type_map = {
            'main': 'Main',
            'trailer': 'Trailer'
        }

        normalized_type = type_map.get(str(type).lower())

        if not normalized_type:
            message = "'type' must be 'Main' or 'Trailer'."
            raise InvalidInput(message)

        input_data = {
            "media_id": media_id,
            "type": normalized_type,
            "version": version
        }

        if track_id is not None:
            input_data["track_id"] = track_id

        return await self.request(
            method="getPlayInfo",
            input=input_data
        )