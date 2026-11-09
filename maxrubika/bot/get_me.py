from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMe:
    async def get_me(self: "maxrubika.Bot"):
        """
        Get information about the authenticated bot.

        Returns:
            Information about the authenticated bot.
        """
        return await self.request(method='getMe')