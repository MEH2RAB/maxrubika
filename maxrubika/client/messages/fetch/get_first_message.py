from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetFirstMessage:
    async def get_first_message(
        self: "maxrubika.Messenger",
        chat: str
    ):
        """
        Get the first message of a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The first message details.
        """
        from ....data import Data

        chat_guid = await self.get_guid(chat)

        interval_result = await self.get_messages_interval(chat_guid, "0")

        if isinstance(interval_result, dict):
            interval_result = Data(interval_result)

        messages = interval_result.find_keys('messages')

        first_message_id = None
        if messages:
            first_msg = Data(messages[0]) if isinstance(messages[0], dict) else messages[0]
            first_message_id = first_msg.find_keys('message_id')

        if not first_message_id:
            no_msg = {"status": "OK", "message": "No messages found in this chat."}
            if getattr(self, 'as_dict', False):
                return no_msg
            return Data(no_msg)

        return await self.get_message_info(chat_guid, first_message_id)