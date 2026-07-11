import maxrubika
from ...data import Data

class SearchChatMessages:
    async def search_chat_messages(
        self: "maxrubika.Client",
        chat: str,
        search_text: str
    ):
        """
        Searches for chat messages based on the specified criteria.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            search_text (str): The text to search for in messages.

        Returns:
            The search results containing messages.
        """
        chat_guid = await self.get_guid(chat)

        result = await self.request(
            method='searchChatMessages',
            input={
                'object_guid': chat_guid,
                'search_text': search_text,
                'type': "Hashtag" if search_text.startswith("#") else "Text"
            }
        )

        result_data = result.to_dict() if hasattr(result, 'to_dict') else result
        message_ids = result_data.get('message_ids', [])

        if not message_ids:
            return Data({"status": "OK", "message": "No messages found."})

        return await self.get_messages_by_id(chat_guid, message_ids)