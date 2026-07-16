import random
from typing import Union, Optional, Literal
from datetime import timedelta, datetime
import time as time_module
import maxrubika
from ..exceptions import InvalidInput

class ForwardMessages:
    async def forward_messages(
        self: "maxrubika.Client",
        from_chat: str,
        message_ids: Union[str, int, list],
        to_chat: str,
        drop_author: bool = False,
        is_mute: bool = False,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
    ):
        """
        Forward specified messages from one chat to another.

        Parameters:
            from_chat (str): The GUID, link, or username of the source chat.
            message_ids (Union[str, int, list]): The IDs of the messages to forward.
            to_chat (str): The GUID, link, or username of the destination chat.
            drop_author (bool): Hide the original sender's identity. Default is False.
            is_mute (bool): Forward silently without notification. Default is False.
            schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
                When to send the forwarded message.
                - Unix timestamp (int/float): Absolute time
                - timedelta: Relative time from now
                - datetime: Absolute date and time
            schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online (u0 only).

        Returns:
            The updated information after forwarding the messages.
        """
        from_chat_guid = await self.get_guid(from_chat)
        to_chat_guid = await self.get_guid(to_chat)

        if not isinstance(message_ids, list):
            message_ids = [message_ids]

        input = {
            'from_object_guid': from_chat_guid,
            'to_object_guid': to_chat_guid,
            'message_ids': message_ids,
            'rnd': random.randint(100000, 999999),
            'drop_author': drop_author,
            'is_mute': is_mute
        }
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
                raise InvalidInput(
                f"Invalid schedule_time type: {type(schedule_time).__name__}")

            if schedule_time <= time_module.time():
                raise InvalidInput("'schedule_time' must be in the future.")

            input['is_scheduled'] = True
            input['schedule_type'] = 'Default'
            input['scheduled_time'] = schedule_time

        elif schedule_type is not None:
            if schedule_type == 'WhenOnline':
                if not to_chat_guid.startswith('u0'):
                    raise InvalidInput(
                        "'schedule_type=WhenOnline' is only available for user chats (private messages)."
                    )
                input['is_scheduled'] = True
                input['schedule_type'] = 'WhenOnline'
            elif schedule_type == 'Default':
                raise InvalidInput(
                    "'schedule_type=Default' requires 'schedule_time' to be provided."
                )

        return await self.request(
            method = 'forwardMessages',
            input = input
        )