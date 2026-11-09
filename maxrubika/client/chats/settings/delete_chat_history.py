from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteChatHistory:
    async def delete_chat_history(
        self: "maxrubika.Messenger",
        chat: str
    ):
        """
        Delete chat history up to the last message.

        Parameters:
            chat (str): The GUID, link, or username of the chat (e.g., user, group).

        Returns:
            Data or dict: The result of the API call.
        """
        from ....data import Data
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if chat_guid.startswith("c0"):
            raise InvalidInput("Cannot delete chat history in channels.")

        last_message = await self.get_last_message(chat_guid)

        if isinstance(last_message, dict):
            last_message = Data(last_message)

        last_message_id = last_message.find_keys('message_id')

        if not last_message_id:
            result_dict = {
                "status": "OK",
                "message": "No messages found to delete."
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        input_data = {
            'object_guid': chat_guid,
            'last_message_id': last_message_id
        }

        return await self.request(
            method='deleteChatHistory',
            input=input_data
        )