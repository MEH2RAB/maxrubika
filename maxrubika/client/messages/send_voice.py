from typing import Union, Optional, Literal
from pathlib import Path
from datetime import timedelta, datetime
import maxrubika
from ..exceptions import InvalidInput

class SendVoice:
    async def send_voice(
        self: "maxrubika.Client",
        chat: str,
        voice: Union[Path, bytes] = None,
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        time: Optional[int] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
        base64: str = None,
        **kwargs
    ):
        """
        Send a voice message to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            voice (Path, bytes, optional): The voice data. Can be a file path or bytes.
            text (Optional[str]): Caption for the voice message. Defaults to None.
            reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
            via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
            time (Optional[int]): Custom duration for the voice message in seconds. Defaults to None (auto-detect).
            schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
                When to send the message.
                - Unix timestamp (int/float): Absolute time
                - timedelta: Relative time from now
                - datetime: Absolute date and time
            schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
            base64 (str, optional): Base64 encoded voice data.

        Returns:
            The API response containing the sent message details.
        """
        if voice is None and base64 is None:
            raise InvalidInput("Either 'voice' or 'base64' must be provided.")

        if voice is not None:
            base64 = None

        return await self.send_message(
            chat=chat,
            text=text,
            reply_to_message_id=reply_to_message_id,
            file_inline=voice,
            type='Voice',
            via_bot=via_bot,
            time=time,
            schedule_time=schedule_time,
            schedule_type=schedule_type,
            base64_data=base64,
            **kwargs
        )