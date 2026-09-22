import maxrubika

class ClearAllDrafts:
    async def clear_all_drafts(self: "maxrubika.Client"):
        """
        Clear all drafts.

        Returns:
            The result of the API call.
        """
        return await self.request(method = 'clearDrafts', input = {'action': 'All'})