from typing import Union, Optional
from asyncio import create_task
import random; import maxrubika
from ..exceptions import InvalidInput

class SendQuiz:
    async def send_quiz(
        self: "maxrubika.Client",
        chat: str,
        question: str,
        options: list,
        correct_option: Union[int, str],
        hint: str = None,
        is_anonymous: bool = True,
        reply_to_message_id: Optional[Union[str, int]] = None,
        auto_delete: Optional[Union[int, float]] = None
    ):
        """
        Send a quiz-type poll message with the specified parameters.

        Parameters:
            chat (str): The GUID or link or username of the chat associated with the quiz (e.g., group, channel).
            question (str): The question for the quiz.
            options (list): A list of string values representing the quiz options.
            correct_option (Union[int, str]): The index or ID of the correct option for quiz-type polls.
            hint (str): A hint for the correct answer in quiz-type polls. Defaults to None.
            is_anonymous (bool): Whether the poll is anonymous or not. Defaults to True.
            reply_to_message_id (Union[str, int]): The ID of the message to reply to. Defaults to None.
            auto_delete (Optional[Union[int, float]]): Auto-delete duration in seconds. Defaults to None.

        Returns:
            The updated information after creating the quiz-type poll.
        """
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
                    raise InvalidInput(
                        f"'correct_option' must be a valid index (0-{len(options)-1}) "
                        f"or one of the option texts: {options}"
                    )
        if not isinstance(correct_option, int):
            raise InvalidInput("'correct_option' must be an integer or string.")

        if correct_option < 0 or correct_option >= len(options):
            raise InvalidInput(
                f"'correct_option' must be between 0 and {len(options) - 1}. "
                f"You provided: {correct_option}"
            )

        if hint and len(hint) > 200:
            raise ValueError("The 'hint' field must not exceed 200 characters.")

        input = {
            'object_guid': chat_guid,
            'question': question,
            'options': options,
            'correct_option_index': correct_option,
            'is_anonymous': is_anonymous,
            'explanation': hint,
            'reply_to_message_id': reply_to_message_id,
            'type': 'Quiz',
            'rnd': random.randint(100000, 999999)
        }

        result = await self.request(method = 'createPoll', input = input)

        if isinstance(auto_delete, (int, float)):
            create_task(self.auto_delete_message(
                result.object_guid, result.message_id, auto_delete))

        return result