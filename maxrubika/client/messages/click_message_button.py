from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class ClickMessageButton:
    async def click_message_button(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[str, int],
        button_id: str
    ):
        """
        Send API call response to a chat's inline keypad button.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): The ID of the message containing inline keyboard.
            button_id (str): The ID of the button.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        msg_result = await self.get_message_info(chat_guid, message_id)
        msg_data = msg_result.to_dict() if hasattr(msg_result, 'to_dict') else msg_result
        message = msg_data.get('message')

        if not message:
            message = f"Message '{message_id}' not found in chat '{chat}'."
            raise InvalidInput(message)

        text = message.get('text', '')

        return await self.request(
            method = 'sendMessageAPICall',
            input = {
                'text': text,
                'object_guid': chat_guid,
                'message_id': str(message_id),
                'aux_data': {'button_id': button_id}
            }
        )