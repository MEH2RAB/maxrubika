import re
import maxrubika
from .exceptions import InvalidInput

class UnbanMember:
    async def unban_member(
        self: "maxrubika.Bot",
        chat_id: str,
        sender_id: str
    ):
        """
        Unban a member from a group or channel.

        Parameters:
            chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0').
            sender_id (str): sender_id of member to unban.

        Returns:
            dict: API response.
        """
        chat_id_regex = r"^(c0|g0|b0)[a-zA-Z0-9]{30}$"
        sender_id_regex = r"^u0[a-zA-Z0-9]{30}$"

        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if chat_id.startswith('b0'):
            raise InvalidInput("'chat_id' must not start with 'b0'.")

        if not re.match(sender_id_regex, sender_id):
            raise InvalidInput("Invalid 'sender_id' format.")

        payload = {
            'chat_id': chat_id,
            'user_id': sender_id
        }
        return await self._request('POST', 'unbanChatMember', json = payload)