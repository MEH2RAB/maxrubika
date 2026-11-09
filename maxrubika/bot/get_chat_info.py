import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChatInfo:
    async def get_chat_info(self: "maxrubika.Bot", chat_id: str):
        """
        Get information about a user, group, or channel.

        Parameters:
            chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0') or user (starts with 'b0').

        Returns:
            The API response with chat information.
        """
        from .exceptions import InvalidInput

        chat_id_regex = r"^(@[a-zA-Z0-9_]{3,32}|(c0|g0|b0)[a-zA-Z0-9]{30})$"

        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        return await self.request(
            method='getChat',
            input={'chat_id': chat_id}
        )