from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SaveMessageDraft:
    async def save_message_draft(
        self: "maxrubika.Messenger",
        chat: str,
        text: str
    ):
        """
        Save a message as a draft in a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat, or 'me'/'cloud'/'self'/'myself'.
            text (str): The draft text content (Max: 4096 chars, 128 lines).

        Returns:
            The result of the API call.
        """
        import random
        from ...exceptions import InvalidInput, MessageTooLong

        if not isinstance(text, str) or not text.strip():
            raise InvalidInput("'text' must be a non-empty string.")

        if len(text) > 4096:
            message = f"Text is too long ({len(text)} characters). Maximum allowed is 4096."
            raise MessageTooLong(message)

        if text.count('\n') > 128:
            message = f"Text has too many lines ({text.count(chr(10))}). Maximum allowed is 128."
            raise MessageTooLong(message)

        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        input_data = {
            'object_guid': chat_guid,
            'text': text.strip(),
            'save_draft_status': 'Save',
            'rnd': random.randint(100000, 999999)
        }
        return await self.request(method='sendMessage', input=input_data)