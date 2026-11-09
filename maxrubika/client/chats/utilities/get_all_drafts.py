from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetAllDrafts:
    async def get_all_drafts(self: "maxrubika.Messenger"):
        """
        Get all saved message drafts.

        Returns:
            The result of the API call containing all drafts.
        """
        return await self.request(method='getAllDrafts')