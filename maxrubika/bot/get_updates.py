import maxrubika

class GetUpdates:
    async def get_updates(
        self: "maxrubika.Bot",
        offset_id: str = None,
        limit: int = 100
    ):
        """
        Fetches new updates (like messages) from the API.

        Parameters:
            offset_id (str, optional): Identifier to fetch subsequent updates. Defaults to None.
            limit (int, optional): Maximum number of updates to retrieve. Defaults to 100.

        Returns:
            dict: The API response including updates and the next_offset_id.
        """
        payload = {}
        if offset_id:
            payload['offset_id'] = offset_id

        if limit is not None:
            payload['limit'] = limit

        return await self._request('POST', 'getUpdates', json = payload)