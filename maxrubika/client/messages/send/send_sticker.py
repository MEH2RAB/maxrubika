from typing import Optional, Union, Literal, TYPE_CHECKING
from datetime import timedelta, datetime
import random
import time as time_module

if TYPE_CHECKING:
    import maxrubika

class SendSticker:
    async def send_sticker(
        self: "maxrubika.Messenger",
        chat: str,
        emoji_character: str,
        sticker_id: str,
        sticker_set_id: str,
        file: dict,
        w_h_ratio: str = '1.0',
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        is_mute: bool = False,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None
    ):
        """
        Send a sticker.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            emoji_character (str): The emoji character associated with the sticker.
            sticker_id (str): The ID of the sticker.
            sticker_set_id (str): The ID of the sticker set.
            file (dict): The file data for the sticker.
            w_h_ratio (str): The width-to-height ratio of the sticker. Defaults to '1.0'.
            reply_to_message_id (Union[str, int], optional): The ID of the message to which this is a reply.
            via_bot (str, optional): Bot GUID or username to send the message via.
            is_mute (bool): If True, the message will be sent silently. Defaults to False.
            schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
            schedule_type (str, optional): 'Default' or 'WhenOnline' (users only).

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        if not isinstance(file, dict):
            if hasattr(file, 'to_dict'):
                file = file.to_dict()
            else:
                raise InvalidInput("'file' must be a dict or Data object.")

        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        sticker_data = {
            'emoji_character': emoji_character,
            'sticker_id': sticker_id,
            'sticker_set_id': sticker_set_id,
            'w_h_ratio': w_h_ratio,
            'file': file
        }

        input_data = {
            'object_guid': chat_guid,
            'reply_to_message_id': reply_to_message_id,
            'rnd': random.randint(100000, 999999),
            'sticker': sticker_data
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

        return await self.request(method='sendMessage', input=input_data)