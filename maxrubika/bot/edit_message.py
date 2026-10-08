from typing import Union, Dict, Any, Optional
import re; import maxrubika
from .metadata import to_metadata
from .exceptions import InvalidInput
from .message_result import MessageResult

class EditMessage:
    async def edit_message(
        self: "maxrubika.Bot",
        chat_id: str,
        message_id: Union[str, int],
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Edits an existing message in a chat.

        Parameters:
            chat_id (str): chat_id of the chat.
            message_id (Union[str, int]): The unique identifier of the message to edit.
            text (str): The new text of the message.
            metadata (dict, optional): Pre-formatted metadata (Bold, Italic, etc.).

        Returns:
            dict: API response with message information.
        """
        if not re.match(r"^(@[a-zA-Z0-9_]{3,32}|(c0|g0|b0)[a-zA-Z0-9]{30})$", chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if not isinstance(text, str) or not text.strip() or len(text) > 4096:
            raise InvalidInput("'text' must be a non-empty string <= 4096 characters.")

        if isinstance(message_id, str):
            if not message_id.isdigit():
                raise InvalidInput("'message_id' string must contain only digits.")
            message_id = int(message_id)

        elif not isinstance(message_id, int):
            raise InvalidInput("'message_id' must be str or int.")

        processed_text = text
        if not metadata:
            try:
                processed = to_metadata(text)
                processed_text = processed['text']
                metadata = processed.get('metadata')
            except Exception:
                processed_text = text
                metadata = None

        payload = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': processed_text
        }
        if metadata:
            payload['metadata'] = metadata

        payload = {k: v for k, v in payload.items() if v is not None}
        result = await self.request('POST', 'editMessageText', json = payload)

        return MessageResult(
            bot=self,
            chat_id=chat_id,
            message_id=message_id,
            result_data=result
        )