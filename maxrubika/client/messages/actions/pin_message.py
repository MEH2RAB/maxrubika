from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class PinMessage:
    async def pin_message(
        self: "maxrubika.Messenger",
        chat: str,
        message_id: Union[str, int]
    ):
        """
        Pin a message.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the message to pin.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        input_data = {
            'object_guid': chat_guid,
            'message_id': message_id,
            'action': 'Pin'
        }

        return await self.request(method='setPinMessage', input=input_data)