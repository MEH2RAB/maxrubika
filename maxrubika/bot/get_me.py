import maxrubika

class GetMe:
    async def get_me(self: "maxrubika.Bot"):
        """
        Get information about the authenticated bot.

        Returns:
            dict: Information about the authenticated bot.
        """
        return await self.request('POST', 'getMe', json = {})