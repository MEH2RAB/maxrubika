import re
from typing import Union
import maxrubika
from .exceptions import InvalidInput

class DeleteMessage:
    async def delete_message(
        self: "maxrubika.Bot",
        chat_id: str,
        message_id: Union[int, str]
    ):
        """
        Provides a method to delete messages.

        Parameters:
            chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0') or user (starts with 'b0').
            message_id (Union[str, int]): message_id of the message to be deleted.

        Returns:
            dict: API response with delete message information.
        """
        chat_id_regex = r"^(c0|g0|b0)[a-zA-Z0-9]{30}$"

        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if isinstance(message_id, str):
            if not message_id.isdigit():
                raise InvalidInput("'message_id' string must contain only digits.")
            message_id = int(message_id)

        elif not isinstance(message_id, int):
            raise InvalidInput("'message_id' must be str or int.")

        payload = {'chat_id': chat_id, 'message_id': message_id}

        return await self._request('POST', 'deleteMessage', json = payload)