from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendMessageAPICall:
    async def send_message_api_call(
        self: "maxrubika.Messenger",
        chat: str,
        message_id: Union[str, int],
        button_id: str
    ):
        """
        Send API call response to a chat's inline keyboard button.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            message_id (Union[str, int]): ID of the message containing inline keyboard.
            button_id (str): ID of the button.

        Returns:
            The result of the API call.

        Example:
            >>> app.send_message_api_call(
            ...     chat="b0C2y04506bd2306f068aa161e0502db",
            ...     message_id="1499338519906784",
            ...     button_id="100"
            ... )
        """
        from ....data import Data
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        msg_result = await self.get_message_info(chat_guid, message_id)

        if isinstance(msg_result, dict):
            msg_result = Data(msg_result)

        message = msg_result.find_keys('message')

        if not message:
            message = f"Message '{message_id}' not found in chat '{chat}'."
            raise InvalidInput(message)

        text = message.find_keys('text')

        input_data = {
            'text': text,
            'object_guid': chat_guid,
            'message_id': str(message_id),
            'aux_data': {'button_id': button_id}
        }

        return await self.request(method='sendMessageAPICall', input=input_data)