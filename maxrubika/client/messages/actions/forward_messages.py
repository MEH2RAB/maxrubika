import random
import time as time_module
from datetime import timedelta, datetime
from typing import Union, List, Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ForwardMessages:
    async def forward_messages(
        self: "maxrubika.Messenger",
        from_chat: str,
        message_ids: Union[str, int, List[Union[str, int]]],
        to_chat: str,
        hide_author: bool = False,
        is_mute: bool = False,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None
    ):
        """
        Forward specified messages from one chat to another.

        Parameters:
            from_chat (str): The GUID, link, or username of the source chat.
            message_ids (Union[str, int, List[Union[str, int]]]): The IDs of the messages to forward.
            to_chat (str): The GUID, link, or username of the destination chat.
            hide_author (bool): Hide the original sender's identity. Default is False.
            is_mute (bool): Forward silently without notification. Default is False.
            schedule_time (Union[int, float, timedelta, datetime], optional): When to send. Unix timestamp, timedelta, or datetime.
            schedule_type (str, optional): 'Default' or 'WhenOnline'. Case-insensitive.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        from_chat_guid = await self.get_guid(from_chat)
        to_chat_guid = await self.get_guid(to_chat)

        if not isinstance(message_ids, list):
            message_ids = [message_ids]

        if not message_ids:
            raise InvalidInput("No message IDs provided for forwarding.")

        scheduled_time = None
        if schedule_time is not None:
            if isinstance(schedule_time, timedelta):
                scheduled_time = int(time_module.time() + schedule_time.total_seconds())
            elif isinstance(schedule_time, datetime):
                scheduled_time = int(schedule_time.timestamp())
            elif isinstance(schedule_time, (int, float)):
                if schedule_time < 1000000000:
                    scheduled_time = int(time_module.time() + schedule_time)
                else:
                    scheduled_time = int(schedule_time)
            else:
                message = f"Invalid schedule_time type: {type(schedule_time).__name__}"
                raise InvalidInput(message)

            if scheduled_time <= time_module.time():
                raise InvalidInput("'schedule_time' must be in the future.")

        normalized_schedule_type = None
        if schedule_type is not None:
            schedule_type_map = {
                'default': 'Default',
                'whenonline': 'WhenOnline',
            }
            normalized_schedule_type = schedule_type_map.get(schedule_type.lower())

            if not normalized_schedule_type:
                raise InvalidInput("'schedule_type' must be 'Default' or 'WhenOnline'.")

        base_input = {
            'from_object_guid': from_chat_guid,
            'to_object_guid': to_chat_guid,
            'drop_author': hide_author,
            'is_mute': is_mute
        }

        if scheduled_time is not None:
            base_input['is_scheduled'] = True
            base_input['schedule_type'] = 'Default'
            base_input['scheduled_time'] = scheduled_time

        elif normalized_schedule_type is not None:
            if normalized_schedule_type == 'WhenOnline':
                if not to_chat_guid.startswith('u0'):
                    raise InvalidInput("'schedule_type=WhenOnline' is only available for user chats (private messages).")
                base_input['is_scheduled'] = True
                base_input['schedule_type'] = 'WhenOnline'
            elif normalized_schedule_type == 'Default':
                raise InvalidInput("'schedule_type=Default' requires 'schedule_time' to be provided.")

        if len(message_ids) > 30:
            chunks = [
                message_ids[i:i + 30]
                for i in range(0, len(message_ids), 30)
            ]

            last_result = None
            for chunk in chunks:
                input_data = {
                    **base_input,
                    'message_ids': chunk,
                    'rnd': random.randint(100000, 999999)
                }
                last_result = await self.request(
                    method='forwardMessages',
                    input=input_data
                )
            return last_result

        input_data = {
            **base_input,
            'message_ids': message_ids,
            'rnd': random.randint(100000, 999999)
        }

        return await self.request(
            method='forwardMessages',
            input=input_data
        )