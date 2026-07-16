import maxrubika

class ResetWallpapers:
    async def reset_wallpapers(self: "maxrubika.Client"):
        """
        Reset all chat wallpapers to default.

        Returns:
            The result of the API call.
        """
        return await self.request(method = 'resetWallpapers')