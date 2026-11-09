import re
from typing import Union, Dict, Any, Optional, List, TYPE_CHECKING

from .keypad_mixin import KeypadMixin
from .message_result import MessageResult

if TYPE_CHECKING:
    import maxrubika

class SendMessage(KeypadMixin):
    async def send_message(
        self: "maxrubika.Bot",
        chat_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        reply_to_message_id: Optional[Union[int, str]] = None,
        disable_notification: bool = False,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ):
        """
        Sends a text message to a chat.

        Parameters:
            chat_id (str): chat_id for the target chat.
            text (str): The text of the message to be sent.
            metadata (dict, optional): Pre-formatted metadata (Bold, Italic, etc.).
            chat_keypad (Dict[str, Any], optional): Custom keyboard attached to the message.
            inline_keypad (Dict[str, Any], optional): Custom inline keyboard attached to the message.
            reply_to_message_id (Union[int, str], optional): If the message is a reply, the original message's ID.
            disable_notification (bool, optional): Sends the message silently.
            resize_keyboard (bool, optional): Requests clients to resize the keyboard vertically.
            one_time_keyboard (bool, optional): Requests clients to hide the keyboard as soon as it's been used.

        Returns:
            API response with message information and action methods.
        """
        from ..data import Data
        from .metadata import to_metadata
        from .exceptions import InvalidInput

        if not re.match(r"^(@[a-zA-Z0-9_]{3,32}|(c0|g0|b0)[a-zA-Z0-9]{30})$", chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        normalized_chat_keypad = self._normalize_keypad(chat_keypad, is_inline=False)
        normalized_inline_keypad = self._normalize_keypad(inline_keypad, is_inline=True)

        processed_text = text
        if not metadata:
            try:
                processed = to_metadata(text)
                processed_text = processed['text']
                metadata = processed.get('metadata')
            except Exception:
                processed_text = text
                metadata = None

        input_data: Dict[str, Any] = {
            'chat_id': chat_id,
            'text': processed_text,
            'disable_notification': disable_notification
        }

        if normalized_chat_keypad:
            normalized_chat_keypad['resize_keyboard'] = resize_keyboard
            normalized_chat_keypad['one_time_keyboard'] = one_time_keyboard
            input_data['chat_keypad'] = normalized_chat_keypad
            input_data['chat_keypad_type'] = 'New'

        if normalized_inline_keypad:
            input_data['inline_keypad'] = normalized_inline_keypad

        if reply_to_message_id is not None:
            input_data['reply_to_message_id'] = str(reply_to_message_id)

        if metadata:
            input_data['metadata'] = metadata

        input_data = {k: v for k, v in input_data.items() if v is not None}

        result = await self.request(
            method='sendMessage',
            input=input_data
        )

        if isinstance(result, dict):
            result = Data(result)

        message_id = result.find_keys("message_id")
        if message_id is not None:
            message_id = str(message_id)

        return MessageResult(
            bot=self,
            chat_id=chat_id,
            message_id=message_id,
            result_data=result
        )