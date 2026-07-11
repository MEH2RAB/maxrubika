import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class DeleteChatHistory:
    async def delete_chat_history(self: "maxrubika.Client", chat: str):
        """
        Delete chat history up to the last message.

        Parameters:
            chat (str): The GUID, link, or username of the chat (e.g., user, group).

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if chat_guid.startswith("c0"):
            raise InvalidInput("Cannot delete chat history in channels.")

        last_message = await self.get_last_message(chat_guid)
        last_message_data = last_message.to_dict() if hasattr(last_message, 'to_dict') else last_message

        last_msg = last_message_data.get("message")
        last_message_id = last_msg.get('message_id') if isinstance(last_msg, dict) else getattr(last_msg, 'message_id', None)

        if not last_message_id:
            return Data({"status": "OK", "message": "No messages found to delete."})

        return await self.request(
            method = 'deleteChatHistory',
            input = {
                'object_guid': chat_guid,
                'last_message_id': last_message_id
            }
        )