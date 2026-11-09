from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetLastMessage:
    async def get_last_message(
        self: "maxrubika.Messenger",
        chat: str
    ):
        """
        Get the last message from a chat and retrieve its details.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The last message details.
        """
        from ....data import Data

        chat_guid = await self.get_guid(chat)

        info_result = await self.get_chat_info(chat_guid)

        if isinstance(info_result, dict):
            info_result = Data(info_result)

        last_message_id = info_result.find_keys('last_message_id')

        if not last_message_id:
            no_msg = {"status": "OK", "message": "No messages found in this chat."}
            if getattr(self, 'as_dict', False):
                return no_msg
            return Data(no_msg)

        return await self.get_message_info(chat_guid, last_message_id)