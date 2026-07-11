from typing import Union
import maxrubika
from ...data import Data

class MarkAsSeen:
    async def mark_as_seen(self: "maxrubika.Client", chat: str, message_id: Union[str, int] = None):
        """
        Mark a specific message as seen.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int], optional): Specific message ID. Defaults to last message.

        Returns:
            Result of the operation.
        """
        chat_guid = await self.get_guid(chat)

        if not message_id:
            last_message = await self.get_last_message(chat_guid)
            if not last_message or not hasattr(last_message, 'message_id'):
                return Data({"status": "OK", "message": "No messages found to mark as seen."})
            message_id = last_message.message_id

        return await self.seen_chats({chat_guid: str(message_id)})