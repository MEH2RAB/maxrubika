from typing import Optional, Union, TYPE_CHECKING
import random
import time as time_module
from datetime import timedelta, datetime

if TYPE_CHECKING:
    import maxrubika

class SendMessage:
    async def send_message(
        self: "maxrubika.Messenger",
        chat: str,
        text: str,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        metadata: Optional[dict] = None,
        is_mute: bool = False,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[str] = None
    ):
        """
        Send a text message to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat, or 'me'/'cloud'/'self'/'myself'.
            text (str): The text content of the message (Max: 4096 chars, 128 lines).
            reply_to_message_id (Union[str, int], optional): The ID of the message to reply to.
            via_bot (str, optional): Bot GUID or username to send the message via.
            metadata (dict, optional): Additional metadata for text formatting.
            is_mute (bool): If True, the message will be sent silently without notification. Defaults to False.
            schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
            schedule_type (str, optional): 'Default' or 'WhenOnline'.

        Returns:
            The result of the API call.
        """
        from ...core import to_metadata
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
            'reply_to_message_id': reply_to_message_id,
            'rnd': random.randint(100000, 999999)
        }
        if is_mute:
            input_data['is_mute'] = True

        if schedule_time is not None:
            if isinstance(schedule_time, timedelta):
                schedule_time = int(time_module.time() + schedule_time.total_seconds())
            elif isinstance(schedule_time, datetime):
                schedule_time = int(schedule_time.timestamp())
            elif isinstance(schedule_time, (int, float)):
                if schedule_time < 1000000000:
                    schedule_time = int(time_module.time() + schedule_time)
                else:
                    schedule_time = int(schedule_time)
            else:
                message = f"Invalid schedule_time type: {type(schedule_time).__name__}"
                raise InvalidInput(message)

            if schedule_time <= time_module.time():
                raise InvalidInput("'schedule_time' must be in the future.")

            input_data['is_scheduled'] = True
            input_data['schedule_type'] = 'Default'
            input_data['scheduled_time'] = schedule_time

        elif schedule_type is not None:
            if schedule_type == 'WhenOnline':
                if not chat_guid.startswith('u0'):
                    raise InvalidInput("'schedule_type=WhenOnline' is only available for user chats.")
                input_data['is_scheduled'] = True
                input_data['schedule_type'] = 'WhenOnline'
            elif schedule_type == 'Default':
                raise InvalidInput("'schedule_type=Default' requires 'schedule_time'.")

        if via_bot is not None:
            bot_guid = await self.get_guid(via_bot)
            if not bot_guid.startswith('b0'):
                message = f"'{via_bot}' does not point to a valid bot. Expected a bot GUID or bot username."
                raise InvalidInput(message)
            input_data['via_bot_guid'] = bot_guid

        processed_text = text
        if not metadata:
            try:
                processed = to_metadata(text)
                processed_text = processed['text']
                metadata = processed.get('metadata')
            except Exception:
                processed_text = text
                metadata = None

        input_data['text'] = processed_text.strip()

        if metadata:
            if 'metadata' in metadata:
                input_data.update(metadata)
            else:
                input_data['metadata'] = metadata

        return await self.request(method='sendMessage', input=input_data)