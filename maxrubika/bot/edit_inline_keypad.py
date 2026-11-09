import re
from typing import Dict, Any, Union, Optional, List, TYPE_CHECKING

from .keypad_mixin import KeypadMixin

if TYPE_CHECKING:
    import maxrubika

class EditInlineKeypad(KeypadMixin):
    async def edit_inline_keypad(
        self: "maxrubika.Bot",
        chat_id: str,
        message_id: Union[str, int],
        inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]
    ) -> Dict[str, Any]:
        """
        Edits the inline keyboard of a specific message in a chat.

        Parameters:
            chat_id (str): chat_id of the chat containing the message. Must be a valid GUID (c0..., g0..., b0...) or a username (@username).
            message_id (str or int): Identifier of the message whose inline keypad should be updated. If passed as a string, it must contain only digits.
            inline_keypad (Dict[str, Any] or List): The new inline keyboard layout. Supports three formats:

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

                Note: Passing an empty list ([]) or None removes the inline keypad from the message.

        Returns:
            API response with message information.
        """
        from .exceptions import InvalidInput

        if not re.match(r"^(@[a-zA-Z0-9_]{3,32}|(c0|g0|b0)[a-zA-Z0-9]{30})$", chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if isinstance(message_id, str):
            if not message_id.isdigit():
                raise InvalidInput("'message_id' string must contain only digits.")
            message_id = int(message_id)
        elif not isinstance(message_id, int):
            raise InvalidInput("'message_id' must be str or int.")

        normalized_inline_keypad = self._normalize_keypad(inline_keypad, is_inline=True)

        input_data = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        if normalized_inline_keypad:
            input_data['inline_keypad'] = normalized_inline_keypad

        input_data = {k: v for k, v in input_data.items() if v is not None}

        return await self.request(
            method='editMessageKeypad',
            input=input_data
        )