import re
import maxrubika
from .exceptions import InvalidInput

class GetChatInfo:
    async def get_chat_info(self: "maxrubika.Bot", chat_id: str):
        """
        Get information about a user, group, or channel.

        Parameters:
            chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0') or user (starts with 'b0').

        Returns:
            dict: API response with chat information.
        """
        chat_id_regex = r"^(c0|g0|b0)[a-zA-Z0-9]{30}$"

        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        payload = {'chat_id': chat_id}
        return await self._request('POST', 'getChat', json = payload)