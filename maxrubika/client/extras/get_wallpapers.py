import maxrubika

class GetWallpapers:
    async def get_wallpapers(self: "maxrubika.Client"):
        """
        Get the current chat wallpaper settings.

        Returns:
            The result of the API call containing wallpaper information.
        """
        return await self.request(method = 'getWallpapers')