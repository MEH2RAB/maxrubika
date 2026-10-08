import re; import maxrubika
from .exceptions import InvalidInput

class RemoveChatKeypad:
    async def remove_chat_keypad(self: "maxrubika.Bot", chat_id: str):
        """
        Removes the custom reply keyboard from the specified chat.

        Parameters:
            chat_id (str): chat_id of the chat where the keypad should be removed.

        Returns:
            The API response after removing the chat keypad.
        """
        chat_id_regex = r"^(@[a-zA-Z0-9_]{3,32}|(c0|g0|b0)[a-zA-Z0-9]{30})$"

        if not re.match(chat_id_regex, chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        payload = {
            'chat_id': chat_id,
            'chat_keypad_type': 'Remove'
        }
        return await self.request('POST', 'editChatKeypad', json = payload)