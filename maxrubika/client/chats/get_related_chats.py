import maxrubika

class GetRelatedChats:
    async def get_related_chats(self: "maxrubika.Client", chat: str):
        """
        Get related chats for a given chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(method = 'getRelatedObjects', input = {'object_guid': chat_guid})