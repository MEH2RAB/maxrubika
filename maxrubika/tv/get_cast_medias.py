from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetCastMedias:
    async def get_cast_medias(
        self: "maxrubika.RubikaTV",
        cast_id: str,
        start_id: Optional[str] = None
    ):
        """
        Retrieve media associated with a cast member.

        Parameters:
            cast_id (str): Identifier of the cast member.
            start_id (str, optional): Optional starting item ID for pagination.

        Returns:
            The API output.
        """
        input_data = {"cast_id": cast_id}

        if start_id is not None:
            input_data["start_id"] = start_id

        return await self.request(
            method="getCastMedias",
            input=input_data
        )