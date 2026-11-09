import re
from typing import Dict, Any, Optional, Union, List, TYPE_CHECKING

from .keypad_mixin import KeypadMixin

if TYPE_CHECKING:
    import maxrubika

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
            chat_keypad (Dict[str, Any] or List): The keyboard layout to set. Supports three formats:

                1. Simple list of strings:
                    [
                        ["Button 1", "Button 2"],
                        ["Button 3"]
                    ]
                    Each inner list is a row. Buttons are strings. The type is set to "Simple" and IDs are assigned automatically starting from 100.

                2. List of tuples: (button_text, button_id, button_type)
                    [
                        [("راهنما", "help")],
                        [("تلاش مجدد", "retry"), ("بستن", "close")],
                        [("پنل مدیریت", "panel", "Simple"), ("تنظیمات", "settings", "Simple")],
                        [("درباره", None), ("پشتیبانی", None)],
                        [("✅ تایید", "confirm"), ("❌ لغو", "cancel"), ("🔄 بازگشت", "back")],
                    ]
                    Tuple structure: (text, id, type) - text: button text, id: button ID (if None, auto-assigned starting from 100), type: button type (if omitted, defaults to "Simple").

                3. Full dictionary (raw API format):
                    {
                        "rows": [
                            {"buttons": [{"id": "1", "button_text": "Button 1", "type": "Simple"}]},
                            {"buttons": [{"id": "2", "button_text": "Button 2", "type": "Simple"}]}
                        ]
                    }

            resize_keyboard (bool, optional): Requests clients to resize the keyboard vertically. Defaults to True.
            one_time_keyboard (bool, optional): Requests clients to hide the keyboard as soon as it's been used. Defaults to False.

        Returns:
            The API response after editing the chat keypad.
        """
        from .exceptions import InvalidInput

        chat_id_regex = r"^(@[a-zA-Z0-9_]{3,32}|(c0|g0|b0)[a-zA-Z0-9]{30})$"
        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if not chat_keypad:
            raise InvalidInput("'chat_keypad' is required. Use remove_chat_keypad() to remove keypad.")

        normalized_keypad = self._normalize_keypad(chat_keypad, is_inline=False)

        if normalized_keypad:
            normalized_keypad['resize_keyboard'] = resize_keyboard
            normalized_keypad['one_time_keyboard'] = one_time_keyboard

        input_data = {
            'chat_id': chat_id,
            'chat_keypad': normalized_keypad,
            'chat_keypad_type': 'New'
        }
        input_data = {k: v for k, v in input_data.items() if v is not None}

        return await self.request(
            method='editChatKeypad',
            input=input_data
        )