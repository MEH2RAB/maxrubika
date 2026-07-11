from typing import Union
import maxrubika

class PinMessage:
    async def pin_message(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[str, int]
    ):
        """
        pin a message.

        Parameters:
            chat (str): The GUID, link, or username of the recipient.
            message_id (Union[str, int]): The ID of the message to pin.

        Returns:
            The update indicating the success of the operation.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'setPinMessage',
            input = {
                'object_guid': chat_guid,
                'message_id': message_id,
                'action': 'Pin'
                }
            )