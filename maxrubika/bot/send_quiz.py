import re
from typing import Union, Dict, Any, Optional, List, TYPE_CHECKING

from .keypad_mixin import KeypadMixin
from .message_result import MessageResult

if TYPE_CHECKING:
    import maxrubika

class SendQuiz(KeypadMixin):
    async def send_quiz(
        self: "maxrubika.Bot",
        chat_id: str,
        question: str,
        options: List[str],
        correct_option: Union[int, str],
        hint: Optional[str] = None,
        is_anonymous: bool = True,
        chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        reply_to_message_id: Optional[Union[int, str]] = None,
        disable_notification: bool = False,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> Dict[str, Any]:
        """
        Send a quiz-type poll message with the specified parameters.

        Parameters:
            chat_id (str): chat_id of the object associated with the quiz (e.g., group or channel).
            question (str): The question for the quiz.
            options (list): A list of string values representing the quiz options.
            correct_option (Union[int, str]): The index or text of the correct option for quiz-type polls.
            hint (str, optional): A hint for the correct answer in quiz-type polls. Defaults to None.
            is_anonymous (bool): Whether the poll is anonymous or not. Defaults to True.
            chat_keypad (Dict, optional): Custom keyboard attached to the message.
            inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
            reply_to_message_id (Union[int, str]): The ID of the message to reply to.
            disable_notification (bool): If set to True, the poll will be sent silently without triggering a notification for users. Defaults to False.
            resize_keyboard (bool): Resize keyboard vertically.
            one_time_keyboard (bool): Hide keyboard after use.

        Returns:
            API response with message information.
        """
        from ..data import Data
        from .exceptions import InvalidInput

        chat_id_regex = r"^(@[a-zA-Z0-9_]{3,32}|(c0|g0|b0)[a-zA-Z0-9]{30})$"

        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if not isinstance(options, (list, tuple)):
            raise InvalidInput("'options' must be a list of strings.")

        if len(options) < 2:
            raise InvalidInput("The 'options' argument must have more than two string values.")

        if len(options) > 10:
            raise InvalidInput("You cannot provide more than 10 options.")

        if len(question) > 255:
            raise InvalidInput("The 'question' field must not exceed 255 characters.")

        for opt in options:
            if not opt.strip():
                raise InvalidInput("Options must not be empty or whitespace-only.")

            if len(opt) > 100:
                raise InvalidInput("Each option must not exceed 100 characters.")

        if isinstance(correct_option, str):
            if correct_option.isdigit():
                correct_option = int(correct_option)
            else:
                found = False
                for i, opt in enumerate(options):
                    if opt == correct_option:
                        correct_option = i
                        found = True
                        break
                if not found:
                    message = f"'correct_option' must be a valid index (0-{len(options)-1}) or one of the option texts: {options}"
                    raise InvalidInput(message)

        if not isinstance(correct_option, int):
            raise InvalidInput("'correct_option' must be an integer or string.")

        if correct_option < 0 or correct_option >= len(options):
            message = f"'correct_option' must be between 0 and {len(options) - 1}. You provided: {correct_option}"
            raise InvalidInput(message)

        if hint and len(hint) > 200:
            raise InvalidInput("The 'hint' field must not exceed 200 characters.")

        normalized_chat_keypad = self._normalize_keypad(chat_keypad, is_inline=False)
        normalized_inline_keypad = self._normalize_keypad(inline_keypad, is_inline=True)

        input_data = {
            'chat_id': chat_id,
            'question': question,
            'options': options,
            'correct_option_index': correct_option,
            'is_anonymous': is_anonymous,
            'type': 'Quiz',
            'disable_notification': disable_notification
        }

        if hint:
            input_data['explanation'] = hint

        if reply_to_message_id is not None:
            input_data['reply_to_message_id'] = reply_to_message_id

        if normalized_chat_keypad:
            normalized_chat_keypad['resize_keyboard'] = resize_keyboard
            normalized_chat_keypad['one_time_keyboard'] = one_time_keyboard
            input_data['chat_keypad'] = normalized_chat_keypad
            input_data['chat_keypad_type'] = 'New'

        if normalized_inline_keypad:
            input_data['inline_keypad'] = normalized_inline_keypad

        input_data = {k: v for k, v in input_data.items() if v is not None}

        result = await self.request(
            method='sendPoll',
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