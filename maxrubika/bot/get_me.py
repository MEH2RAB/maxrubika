import maxrubika

class GetMe:
    async def get_me(self: "maxrubika.Bot"):
        """
        Get information about the authenticated bot.

        Returns:
            dict: Information about the authenticated bot.
        """
        payload = {}
        return await self._request('POST', 'getMe', json = payload)