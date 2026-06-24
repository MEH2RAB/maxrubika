import re
from typing import Union
import maxrubika
from .exceptions import InvalidInput

class ForwardMessage:
    async def forward_message(
        self: "maxrubika.Bot",
        from_chat_id: str,
        message_id: Union[str, int],
        to_chat_id: str,
        disable_notification: bool = False
    ):
        """
        Provides a method to forward messages.

        Parameters:
            from_chat_id (str): chat_id of the source object from which messages are forwarded.
            message_id (str): message_id of the message to be frowarded.
            to_chat_id (str): chat_id of the destination object to which messages are forwarded.
            disable_notification (bool): If set to True, the message will be sent silently without triggering a notification for users. Defaults to False.

        Returns:
            dict: API response with message information.
        """
        chat_id_regex = r"^(c0|g0|b0)[a-zA-Z0-9]{30}$"

        if not re.match(chat_id_regex, from_chat_id):
            raise InvalidInput("Invalid 'from_chat_id' format.")

        if not re.match(chat_id_regex, to_chat_id):
            raise InvalidInput("Invalid 'to_chat_id' format.")

        if isinstance(message_id, str):
            if not message_id.isdigit():
                raise InvalidInput("'message_id' string must contain only digits.")
            message_id = int(message_id)

        elif not isinstance(message_id, int):
            raise InvalidInput("'message_id' must be str or int.")

        payload = {
            'from_chat_id': from_chat_id,
            'message_id': message_id,
            'to_chat_id': to_chat_id,
            'disable_notification': disable_notification
        }
        return await self._request('POST', 'forwardMessage', json = payload)