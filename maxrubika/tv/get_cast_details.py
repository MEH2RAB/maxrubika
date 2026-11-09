from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetCastDetails:
    async def get_cast_details(
        self: "maxrubika.RubikaTV",
        cast_id: str
    ):
        """
        Retrieve details of a cast member.

        Parameters:
            cast_id (str): Identifier of the cast member.

        Returns:
            The API output.
        """
        return await self.request(
            method="getCastDetails",
            input={"cast_id": cast_id}
        )