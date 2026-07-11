import maxrubika
from ...data import Data

class GetFirstMessage:
    async def get_first_message(self: "maxrubika.Client", chat: str):
        """
        Get the first message of a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The first message details.
        """
        chat_guid = await self.get_guid(chat)

        interval_result = await self.get_messages_interval(chat_guid, "0")

        first_message_id = None

        if hasattr(interval_result, 'messages') and interval_result.messages:
            first_msg = interval_result.messages[0]
            first_message_id = int(first_msg.message_id) if hasattr(first_msg, 'message_id') else None
        else:
            interval_data = interval_result.to_dict() if hasattr(interval_result, 'to_dict') else interval_result
            messages = interval_data.get('messages', [])
            if messages:
                first_message_id = int(messages[0].get('message_id')) if isinstance(messages[0], dict) else int(messages[0].message_id)

        if not first_message_id:
            return Data({"status": "OK", "message": "No messages found in this chat."})

        return await self.get_message_info(chat_guid, first_message_id)