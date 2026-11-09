from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetThemes:
    async def get_themes(self: "maxrubika.Messenger"):
        """
        Get the list of available themes.

        Returns:
            The result of the API call, containing the list of themes.
        """
        return await self.request(method='getThemes')