from typing import Union, Optional
import maxrubika
from ..core.metadata import to_metadata

class EditMessage:
    async def edit_message(
        self: "maxrubika.Client",
        chat: str,
        message_id: Union[int, str],
        text: str,
        metadata: Optional[dict] = None
    ):
        """
        Edit the specified message associated with the given chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat associated with the message
                (e.g., user, group, channel).
            message_id (Union[int, str]): The ID of the message to be edited.
            text (str): The new text content for the message.
            metadata (dict, optional): Pre-formatted metadata (Bold, Italic, etc.).

        Returns:
            The updated information after editing the message.
        """
        chat_guid = await self.get_guid(chat)

        processed_text = text
        if not metadata:
            try:
                processed = to_metadata(text)
                processed_text = processed['text']
                metadata = processed.get('metadata')
            except Exception:
                processed_text = text
                metadata = None

        input = {
            'object_guid': chat_guid,
            'message_id': message_id,
            'text': processed_text
        }

        if metadata:
            input['metadata'] = metadata

        return await self.request(method = 'editMessage', input = input)