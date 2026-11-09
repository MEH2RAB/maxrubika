from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetSuggestedFolders:
    async def get_suggested_folders(self: "maxrubika.Messenger"):
        """
        Get the suggested folders for the user.

        Returns:
            The suggested folders for the user.
        """
        return await self.request(method='getSuggestedFolders')