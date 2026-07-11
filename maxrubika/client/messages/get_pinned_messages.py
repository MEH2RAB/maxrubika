import maxrubika
from ...data import Data

class GetPinnedMessages:
    async def get_pinned_messages(
        self: "maxrubika.Client",
        chat: str
    ):
        """
        Get all pinned messages from a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            Data: Dictionary containing pinned messages and optionally message IDs.
        """
        chat_guid = await self.get_guid(chat)

        chat_info = await self.get_chat_info(chat_guid)
        chat_data = chat_info.to_dict() if hasattr(chat_info, 'to_dict') else chat_info
        chat = chat_data.get('chat', {})

        pinned_ids = chat.get('pinned_message_ids')

        if not pinned_ids:
            return Data({"status": "OK", "message": "No pinned messages."})

        messages_result = await self.get_messages_by_id(chat_guid, pinned_ids)
        messages_data = messages_result.to_dict() if hasattr(messages_result, 'to_dict') else messages_result
        messages = messages_data.get('messages', [])

        return Data({
            "messages": messages,
            "count": len(messages),
            "pinned_ids": pinned_ids
        })