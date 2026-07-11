from typing import Union
import maxrubika

class UnpinMessage:
    async def unpin_message(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[str, int]
    ):
        """
        unpin a message.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the message to unpin.

        Returns:
            The update indicating the success of the operation.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'setPinMessage',
            input = {
                'object_guid': chat_guid,
                'message_id': message_id,
                'action': 'Unpin'
                }
            )