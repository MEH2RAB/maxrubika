from typing import Union, Optional
from asyncio import create_task
import random; import maxrubika
from ..exceptions import InvalidInput

class SendPoll:
    async def send_poll(
        self: "maxrubika.Client",
        chat: str,
        question: str,
        options: list,
        is_anonymous: bool = True,
        multiple_answers: bool = False,
        reply_to_message_id: Optional[Union[str, int]] = None,
        auto_delete: Optional[Union[int, float]] = None
    ):
        """
        Send a poll message with the specified parameters.

        Parameters:
            chat (str): The GUID, link or username of the chat associated with the poll (e.g., group, channel).
            question (str): The question for the poll.
            options (list): A list of string values representing the poll options.
            is_anonymous (bool): Whether the poll is anonymous or not. Defaults to True.
            multiple_answers (bool): Whether the poll allows multiple answers or not. Defaults to False.
            reply_to_message_id (Optional[Union[str, int]]): The ID of the message to reply to. Defaults to None.
            auto_delete (Optional[Union[int, float]]): Auto-delete duration in seconds. Defaults to None.

        Returns:
            The updated information after creating the poll.
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

        input = {
            'object_guid': chat_guid,
            'question': question,
            'options': options,
            'is_anonymous': is_anonymous,
            'allows_multiple_answers': multiple_answers,
            'reply_to_message_id': reply_to_message_id,
            'type': 'Regular',
            'rnd': random.randint(100000, 999999)
        }
        result = await self.request(method = 'createPoll', input = input)

        if isinstance(auto_delete, (int, float)):
            create_task(self.auto_delete_message(
                result.object_guid, result.message_id, auto_delete))

        return result