from typing import Union, Dict, Any, Optional, List
import re; import maxrubika
from .metadata import to_metadata
from .keypad_mixin import KeypadMixin
from .exceptions import InvalidInput

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
    ) -> Dict[str, Any]:
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
            dict: API response with message information.
        """
        if not re.match(r"^(c0|g0|b0)[a-zA-Z0-9]{30}$", chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if not isinstance(text, str) or len(text) > 4096:
            raise InvalidInput("'text' must be a string <= 4096 characters.")

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

        payload: Dict[str, Any] = {
            'chat_id': chat_id,
            'text': processed_text,
            'disable_notification': disable_notification
        }

        if normalized_chat_keypad:
            normalized_chat_keypad['resize_keyboard'] = resize_keyboard
            normalized_chat_keypad['one_time_keyboard'] = one_time_keyboard
            payload['chat_keypad'] = normalized_chat_keypad
            payload['chat_keypad_type'] = 'New'

        if normalized_inline_keypad:
            payload['inline_keypad'] = normalized_inline_keypad

        if reply_to_message_id is not None:
            payload['reply_to_message_id'] = str(reply_to_message_id)

        if metadata:
            payload['metadata'] = metadata

        payload = {k: v for k, v in payload.items() if v is not None}
        return await self._request('POST', 'sendMessage', json = payload)