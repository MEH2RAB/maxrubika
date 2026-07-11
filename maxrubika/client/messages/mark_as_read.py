from typing import Union
import maxrubika
from ...data import Data

class MarkAsRead:
    async def mark_as_read(self: "maxrubika.Client", chat: str):
        """
        Mark a chat as read by seeing the last message.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            Result of the operation.
        """
        chat_guid = await self.get_guid(chat)

        last_message = await self.get_last_message(chat_guid)

        if not last_message or not hasattr(last_message, 'message_id'):
            return Data({"status": "OK", "message": "No messages found to mark as read."})

        message_id = last_message.message_id
        return await self.seen_chats({chat_guid: message_id})