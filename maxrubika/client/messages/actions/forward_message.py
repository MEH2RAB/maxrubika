from typing import Union, Optional, Literal, TYPE_CHECKING
from datetime import timedelta, datetime

if TYPE_CHECKING:
    import maxrubika

class ForwardMessage:
    async def forward_message(
        self: "maxrubika.Messenger",
        from_chat: str,
        message_id: Union[str, int],
        to_chat: str,
        hide_author: bool = False,
        is_mute: bool = False,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None
    ):
        """
        Forward a single message from one chat to another.

        Parameters:
            from_chat (str): The GUID, link, or username of the source chat.
            message_id (Union[str, int]): The ID of the message to forward.
            to_chat (str): The GUID, link, or username of the destination chat.
            hide_author (bool): Hide the original sender's identity. Default is False.
            is_mute (bool): Forward silently without notification. Default is False.
            schedule_time (Optional[Union[int, float, timedelta, datetime]]):
                When to send the forwarded message.
            schedule_type (Optional[Literal['Default', 'WhenOnline']]):
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online.

        Returns:
            The result of the API call.
        """
        return await self.forward_messages(
            from_chat=from_chat,
            message_ids=[message_id],
            to_chat=to_chat,
            hide_author=hide_author,
            is_mute=is_mute,
            schedule_time=schedule_time,
            schedule_type=schedule_type
        )