from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetWishList:
    async def get_wish_list(
        self: "maxrubika.RubikaTV",
        start_id: Optional[str] = None
    ):
        """
        Retrieve the wishlist items.

        Parameters:
            start_id (str, optional): Optional starting item ID for pagination.

        Returns:
            The API output.
        """
        input_data = {}

        if start_id is not None:
            input_data["start_id"] = start_id

        return await self.request(
            method="getWishList",
            input=input_data
        )