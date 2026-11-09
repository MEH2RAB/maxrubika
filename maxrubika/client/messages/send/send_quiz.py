from typing import Union, Optional, TYPE_CHECKING
import random

if TYPE_CHECKING:
    import maxrubika

class SendQuiz:
    async def send_quiz(
        self: "maxrubika.Messenger",
        chat: str,
        question: str,
        options: list,
        correct_option: Union[int, str],
        hint: Optional[str] = None,
        is_anonymous: bool = True,
        reply_to_message_id: Optional[Union[str, int]] = None,
        is_mute: bool = False
    ):
        """
        Send a quiz-type poll message.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            question (str): The question for the quiz (Max: 255 chars).
            options (list): A list of quiz options (2 to 10 items, each Max: 100 chars).
            correct_option (Union[int, str]): The index or text of the correct option.
            hint (str, optional): A hint for the correct answer (Max: 200 chars).
            is_anonymous (bool): Whether the poll is anonymous. Defaults to True.
            reply_to_message_id (Union[str, int], optional): The ID of the message to reply to.
            is_mute (bool): Whether the quiz message is sent silently. Defaults to False.

        Returns:
            The updated information after creating the quiz-type poll.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0", "b0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

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

        input_data = {
            'object_guid': chat_guid,
            'question': question,
            'options': options,
            'correct_option_index': correct_option,
            'is_anonymous': is_anonymous,
            'explanation': hint,
            'reply_to_message_id': reply_to_message_id,
            'is_mute': is_mute,
            'type': 'Quiz',
            'rnd': random.randint(100000, 999999)
        }

        return await self.request(method='createPoll', input=input_data)