from typing import Dict, Any, Optional, Union, List
import re; import maxrubika
from .keypad_mixin import KeypadMixin
from .exceptions import InvalidInput

class EditChatKeypad(KeypadMixin):
    async def edit_chat_keypad(
        self: "maxrubika.Bot",
        chat_id: str,
        chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]],
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> Dict[str, Any]:
        """
        Edits or adds a new chat keypad (custom keyboard) to the chat.

        Parameters:
            chat_id (str): chat_id of the group (starts with 'g0') or user (starts with 'b0').
            chat_keypad (Dict[str, Any] or List): The keyboard layout to set.
            resize_keyboard (bool, optional): Requests clients to resize the keyboard vertically. 
                Defaults to True.
            one_time_keyboard (bool, optional): Requests clients to hide the keyboard as soon as it's been used. 
                Defaults to False.

        Returns:
            The API response after editing the chat keypad.

        Examples:
            # روش 1: لیست دو بعدی ساده
            chat_keypad = [
                ["Button 1"],
                ["Button 2"]
            ]
            bot.edit_chat_keypad("b0abc123...", chat_keypad)

            # روش 2: دیکشنری کامل
            chat_keypad = {
                "rows": [
                    {"buttons": [{"id": "1", "button_text": "Button 1", "type": "Simple"}]},
                    {"buttons": [{"id": "2", "button_text": "Button 2", "type": "Simple"}]}
                ]
            }
            bot.edit_chat_keypad("b0abc123...", chat_keypad)
        """
        chat_id_regex = r"^(c0|g0|b0)[a-zA-Z0-9]{30}$"
        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if chat_id.startswith('c0') or chat_id.startswith('g0'):
            raise InvalidInput("Chat keypad cannot be set for groups or channels.")

        if not chat_keypad:
            raise InvalidInput("'chat_keypad' is required. Use remove_chat_keypad() to remove keypad.")

        normalized_keypad = self._normalize_keypad(chat_keypad, is_inline=False)

        if normalized_keypad:
            normalized_keypad['resize_keyboard'] = resize_keyboard
            normalized_keypad['one_time_keyboard'] = one_time_keyboard

        payload = {
            'chat_id': chat_id,
            'chat_keypad': normalized_keypad,
            'chat_keypad_type': 'New'
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        return await self._request('POST', 'editChatKeypad', json = payload)