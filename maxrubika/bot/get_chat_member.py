from typing import Any, Dict, Union
import re; import maxrubika
from .exceptions import InvalidInput

class GetChatMember:
    async def get_chat_member(
        self: "maxrubika.Bot",
        chat_id: str,
        user_id: str
    ):
        """
        Get information about a single member of a chat.

        Parameters:
            chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0').
            user_id (str): user_id of member to look up (starts with 'u0').

        Returns:
            dict: API response.
        """
        chat_id_regex = r"^(@[a-zA-Z0-9_]{3,32}|(c0|g0|b0)[a-zA-Z0-9]{30})$"
        user_id_regex = r"^u0[a-zA-Z0-9]{30}$"

        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if chat_id.startswith('b0'):
            raise InvalidInput("'chat_id' must not start with 'b0'.")

        if not re.match(user_id_regex, user_id):
            raise InvalidInput("Invalid 'user_id' format.")

        payload = {
            'chat_id': chat_id,
            'user_id': user_id
        }
        return await self.request('POST', 'getChatMember', json = payload)