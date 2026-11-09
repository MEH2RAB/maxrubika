from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMediaByLink:
    async def get_media_by_link(
        self: "maxrubika.RubikaTV",
        link: str,
        track_id: Optional[str] = None
    ):
        """
        Retrieve media details by its share link.

        Parameters:
            link (str): Share link (e.g., "https://rubika.ir/vod/294119").
            track_id (str, optional): Optional tracking identifier (session hash string).

        Returns:
            The API output.
        """
        from .exceptions import InvalidInput

        stripped = link.rstrip("/").split("/")[-1]

        if not stripped.isdigit():
            message = f"Could not extract a numeric media ID from '{link}'."
            raise InvalidInput(message)

        input_data = {"share_string": stripped}

        if track_id is not None:
            input_data["track_id"] = track_id

        return await self.request(
            method="getMediaByShareString",
            input=input_data
        )