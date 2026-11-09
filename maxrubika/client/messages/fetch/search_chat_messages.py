from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SearchChatMessages:
    async def search_chat_messages(
        self: "maxrubika.Messenger",
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
        from ....data import Data

        chat_guid = await self.get_guid(chat)

        is_hashtag = search_text.startswith('#')

        input_data = {
            'object_guid': chat_guid,
            'search_text': search_text[1:] if is_hashtag else search_text,
            'type': "Hashtag" if is_hashtag else "Text"
        }

        result = await self.request(
            method='searchChatMessages',
            input=input_data
        )

        if isinstance(result, dict):
            result = Data(result)

        message_ids = result.find_keys('message_ids') or []

        if not message_ids:
            no_msg = {"status": "OK", "message": "No messages found."}
            if getattr(self, 'as_dict', False):
                return no_msg
            return Data(no_msg)

        return await self.get_messages_by_id(chat_guid, message_ids)