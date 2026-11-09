from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ResetWallpapers:
    async def reset_wallpapers(self: "maxrubika.Messenger"):
        """
        Reset all chat wallpapers to default.

        Returns:
            The result of the API call.
        """
        return await self.request(method='resetWallpapers')