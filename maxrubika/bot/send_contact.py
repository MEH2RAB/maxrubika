from typing import Union, Dict, Any, Optional, List
import re; import maxrubika
from .keypad_mixin import KeypadMixin
from .exceptions import InvalidInput

class SendContact(KeypadMixin):
    async def send_contact(
        self: "maxrubika.Bot",
        chat_id: str,
        phone_number: str,
        first_name: str,
        last_name: str = '',
        chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        reply_to_message_id: Optional[Union[int, str]] = None,
        disable_notification: bool = False,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> Dict[str, Any]:
        """
        Sends a contact message to a chat.

        Parameters:
            chat_id (str): chat_id for the target chat.
            phone_number (str): Contact's phone number.
            first_name (str): Contact's first name.
            last_name (str, optional): Contact's last name. Defaults to ' '.
            chat_keypad (Dict[str, Any], optional): Custom keyboard attached to the message. Defaults to None.
            inline_keypad (Dict[str, Any], optional): Custom inline keyboard attached to the message. Defaults to None.
            reply_to_message_id (Union[int, str], optional): If the message is a reply, the original message's ID. Defaults to None.
            disable_notification (bool, optional): Sends the message silently. Users will not receive a notification. Defaults to False.
            resize_keyboard (bool, optional): Requests clients to resize the keyboard vertically. Defaults to True.
            one_time_keyboard (bool, optional): Requests clients to hide the keyboard as soon as it's been used. Defaults to False.

        Returns:
            dict: API response with message information.
        """
        if not re.match(r"^(c0|g0|b0)[a-zA-Z0-9]{30}$", chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if not phone_number or not isinstance(phone_number, str):
            raise InvalidInput("'phone_number' must be a non-empty string.")

        if not first_name or not isinstance(first_name, str):
            raise InvalidInput("'first_name' must be a non-empty string.")

        normalized_chat_keypad = self._normalize_keypad(chat_keypad, is_inline=False)
        normalized_inline_keypad = self._normalize_keypad(inline_keypad, is_inline=True)

        payload: Dict[str, Any] = {
            'chat_id': chat_id,
            'phone_number': phone_number,
            'first_name': first_name,
            'last_name': last_name,
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
            payload['reply_to_message_id'] = reply_to_message_id

        payload = {k: v for k, v in payload.items() if v is not None}
        return await self._request('POST', 'sendContact', json = payload)