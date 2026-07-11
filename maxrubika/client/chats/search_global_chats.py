import maxrubika

class SearchGlobalChats:
    async def search_global_chats(self: "maxrubika.Client", text: str):
        """
        Search for global chats (users, channels, etc.) based on the given search text.

        Parameters:
            text (str): The text to search for.

        Returns:
            The update containing search results.
        """
        return await self.request(method = 'searchGlobalObjects', input = {'search_text': text})
