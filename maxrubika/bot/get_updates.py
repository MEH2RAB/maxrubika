from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetUpdates:
    async def get_updates(
        self: "maxrubika.Bot",
        offset_id: Optional[str] = None,
        limit: int = 100
    ):
        """
        Fetches new updates (like messages) from the API.

        Parameters:
            offset_id (str, optional): Identifier to fetch subsequent updates. Defaults to None.
            limit (int, optional): Maximum number of updates to retrieve. Defaults to 100.

        Returns:
            The API response including updates and the next_offset_id.
        """
        input_data = {}

        if offset_id:
            input_data['offset_id'] = offset_id

        if limit is not None:
            input_data['limit'] = limit

        return await self.request(
            method='getUpdates',
            input=input_data
        )