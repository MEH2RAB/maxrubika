from typing import Union, Dict, Any, Optional, List
import re; import maxrubika
from .keypad_mixin import KeypadMixin
from .exceptions import InvalidInput

class SendPoll(KeypadMixin):
    async def send_poll(
        self: "maxrubika.Bot",
        chat_id: str,
        question: str,
        options: List[str],
        is_anonymous: bool = True,
        multi_select: bool = False,
        chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        reply_to_message_id: Optional[Union[int, str]] = None,
        disable_notification: bool = False,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> Dict[str, Any]:
        """
        Send a poll message with the specified parameters.

        Parameters:
            chat_id (str): chat_id of the object associated with the poll (e.g., group or channel).
            question (str): The question for the poll.
            options (list): A list of string values representing the poll options.
            is_anonymous (bool): Whether the poll is anonymous or not. Defaults to True.
            multi_select (bool): Whether the poll allows multiple answers or not. Defaults to False.
            chat_keypad (Dict, optional): Custom keyboard attached to the message.
            inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
            reply_to_message_id (Union[str, int]): The ID of the message to reply to.
            disable_notification (bool): If set to True, the poll will be sent silently without triggering a notification for users. Defaults to False.
            resize_keyboard (bool): Resize keyboard vertically.
            one_time_keyboard (bool): Hide keyboard after use.

        Returns:
            dict: API response with message information.
        """
        chat_id_regex = r"^(c0|g0|b0)[a-zA-Z0-9]{30}$"

        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if len(options) < 2:
            raise InvalidInput("The 'options' argument must have more than two string values.")

        if len(options) > 10:
            raise InvalidInput("You cannot provide more than 10 options.")

        if len(question) > 255:
            raise InvalidInput("The 'question' field must not exceed 255 characters.")

        for opt in options:
            if not opt.strip():
                raise InvalidInput("'Options' must not be empty or whitespace-only.")

            if len(opt) > 100:
                raise InvalidInput("Each option must not exceed 100 characters.")

        normalized_chat_keypad = self._normalize_keypad(chat_keypad, is_inline=False)
        normalized_inline_keypad = self._normalize_keypad(inline_keypad, is_inline=True)

        payload: Dict[str, Any] = {
            'chat_id': chat_id,
            'question': question,
            'options': options,
            'is_anonymous': is_anonymous,
            'allows_multiple_answers': multi_select,
            'type': 'Regular',
            'disable_notification': disable_notification
        }

        if reply_to_message_id is not None:
            payload['reply_to_message_id'] = reply_to_message_id

        if normalized_chat_keypad:
            normalized_chat_keypad['resize_keyboard'] = resize_keyboard
            normalized_chat_keypad['one_time_keyboard'] = one_time_keyboard
            payload['chat_keypad'] = normalized_chat_keypad
            payload['chat_keypad_type'] = 'New'

        if normalized_inline_keypad:
            payload['inline_keypad'] = normalized_inline_keypad

        payload = {k: v for k, v in payload.items() if v is not None}
        return await self._request('POST', 'sendPoll', json = payload)