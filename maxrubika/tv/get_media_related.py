from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMediaRelated:
    async def get_media_related(
        self: "maxrubika.RubikaTV",
        media_id: str,
        section_type: Optional[Literal["PageRelated", "EndOfStream"]] = None,
        start_id: Optional[str] = None
    ):
        """
        Retrieve media related to a specific media.

        Parameters:
            media_id (str): Identifier of the media.
            section_type (str, optional): Optional section type. One of: "PageRelated", "EndOfStream".
            start_id (str, optional): Optional starting item ID for pagination.

        Returns:
            The API output.
        """
        input_data = {"media_id": media_id}

        if section_type is not None:
            input_data["section_type"] = section_type

        if start_id is not None:
            input_data["start_id"] = start_id

        return await self.request(
            method="getRelated",
            input=input_data
        )