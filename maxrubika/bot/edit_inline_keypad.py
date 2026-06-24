from typing import Dict, Any, Union, Optional, List
import re; import maxrubika
from .keypad_mixin import KeypadMixin
from .exceptions import InvalidInput

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
            chat_id (str): chat_id of the chat containing the message.
            message_id (str or int): Identifier of the message whose inline keypad should be updated.
            inline_keypad (Dict[str, Any] or List): A dictionary or list representing the new inline keyboard layout.

        Returns:
            dict: API response with message information.

        Examples:
            # روش 1: لیست دو بعدی ساده
            inline_keypad = [
                ["Button 1"],
                ["Button 2"]
            ]
            bot.edit_inline_keypad("b0abc123...", "message_id", inline_keypad)

            # روش 2: دیکشنری کامل
            inline_keypad = {
                "rows": [
                    {"buttons": [{"id": "1", "button_text": "Button 1", "type": "Simple"}]},
                    {"buttons": [{"id": "2", "button_text": "Button 2", "type": "Simple"}]}
                ]
            }
            bot.edit_inline_keypad("b0abc123...", "message_id", inline_keypad)
        """
        if not re.match(r"^(c0|g0|b0)[a-zA-Z0-9]{30}$", chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if chat_id.startswith('c0') or chat_id.startswith('g0'):
            raise InvalidInput("Inline keypad cannot be set for groups or channels.")

        if isinstance(message_id, str):
            if not message_id.isdigit():
                raise InvalidInput("'message_id' string must contain only digits.")
            message_id = int(message_id)

        elif not isinstance(message_id, int):
            raise InvalidInput("'message_id' must be str or int.")

        normalized_inline_keypad = self._normalize_keypad(inline_keypad, is_inline = True)

        payload: Dict[str, Any] = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        if normalized_inline_keypad:
            payload['inline_keypad'] = normalized_inline_keypad

        payload = {k: v for k, v in payload.items() if v is not None}
        return await self._request('POST', 'editMessageKeypad', json = payload)