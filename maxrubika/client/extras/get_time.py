from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetTime:
    async def get_time(self: "maxrubika.Messenger"):
        """
        Retrieve the current server time.

        Returns:
            The result of the API call.
        """
        return await self.request(method='getTime')