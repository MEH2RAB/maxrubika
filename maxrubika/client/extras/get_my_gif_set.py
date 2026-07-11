import maxrubika

class GetMyGifSet:
    async def get_my_gif_set(self: "maxrubika.Client"):
        """
        Gets the user's personal GIF set.

        Returns:
            Information about the user's GIF set.
        """
        return await self.request(method = 'getMyGifSet')