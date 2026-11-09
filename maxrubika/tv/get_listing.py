from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetListing:
    async def get_listing(
        self: "maxrubika.RubikaTV",
        listing_id: str = "home"
    ):
        """
        Retrieve a listing (e.g., home page sections).

        Parameters:
            listing_id (str): Identifier of the listing (default: "home").

        Returns:
            The API output.
        """
        return await self.request(
            method="getListing",
            input={"listing_id": listing_id}
        )