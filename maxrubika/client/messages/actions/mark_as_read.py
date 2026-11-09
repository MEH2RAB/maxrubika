from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class MarkAsRead:
    async def mark_as_read(
        self: "maxrubika.Messenger",
        chat: str
    ):
        """
        Mark a chat as read by seeing the last message.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            Result of the operation.
        """
        from ....data import Data

        chat_guid = await self.get_guid(chat)

        last_message = await self.get_last_message(chat_guid)

        if isinstance(last_message, dict):
            last_message = Data(last_message)

        message_id = last_message.find_keys('message_id')

        if not message_id:
            no_msg = {"status": "OK", "message": "No messages found to mark as read."}
            if getattr(self, 'as_dict', False):
                return no_msg
            return Data(no_msg)

        return await self.seen_chats({chat_guid: message_id})