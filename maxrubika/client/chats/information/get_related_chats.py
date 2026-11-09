from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetRelatedChats:
    async def get_related_chats(
        self: "maxrubika.Messenger",
        chat: str,
        start_id: Optional[str] = None
    ):
        """
        Get related chats for a given chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            start_id (str, optional): Starting item ID for pagination.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {'object_guid': chat_guid}

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(method='getRelatedObjects', input=input_data)