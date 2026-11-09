import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class BanMember:
    async def ban_member(
        self: "maxrubika.Bot",
        chat_id: str,
        sender_id: str
    ):
        """
        Ban a member from a group or channel.

        Parameters:
            chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0').
            sender_id (str): sender_id of member to ban (starts with 'u0').

        Returns:
            The API response.
        """
        from .exceptions import InvalidInput

        chat_id_regex = r"^(@[a-zA-Z0-9_]{3,32}|(c0|g0|b0)[a-zA-Z0-9]{30})$"
        sender_id_regex = r"^u0[a-zA-Z0-9]{30}$"

        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if chat_id.startswith('b0'):
            raise InvalidInput("'chat_id' must not start with 'b0'.")

        if not re.match(sender_id_regex, sender_id):
            raise InvalidInput("Invalid 'sender_id' format.")

        input_data = {
            'chat_id': chat_id,
            'user_id': sender_id
        }

        return await self.request(
            method='banChatMember',
            input=input_data
        )