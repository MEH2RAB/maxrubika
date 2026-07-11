import maxrubika

class GetTime:
    async def get_time(self: "maxrubika.Client"):
        """
        Retrieve the current server time.

        Returns:
            The result of the API call.
        """
        return await self.request(method = "getTime")