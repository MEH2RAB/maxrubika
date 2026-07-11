import maxrubika
from ...data import Data

class GetLastMessage:
    async def get_last_message(self: "maxrubika.Client", chat: str):
        """
        Get the last message from a chat and retrieve its details.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The last message details.
        """
        chat_guid = await self.get_guid(chat)

        info_result = await self.get_chat_info(chat_guid)
        info_data = info_result.to_dict() if hasattr(info_result, 'to_dict') else info_result

        chat_obj = info_data.get('chat', {})
        last_message_obj = chat_obj.get('last_message', {})

        last_message_id = last_message_obj.get('message_id') if isinstance(last_message_obj, dict) else None

        if not last_message_id:
            return Data({"status": "OK", "message": "No messages found in this chat."})

        return await self.get_message_info(chat_guid, last_message_id)