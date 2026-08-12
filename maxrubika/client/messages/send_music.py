from typing import Union, Optional, Literal
from pathlib import Path
from datetime import timedelta, datetime
import maxrubika
from ..exceptions import InvalidInput

class SendMusic:
    async def send_music(
        self: "maxrubika.Client",
        chat: str,
        music: Union[Path, bytes] = None,
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        performer: Optional[str] = None,
        time: Optional[int] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
        base64: str = None,
        **kwargs
    ):
        """
        Send a music file to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            music (Path, bytes, optional): The music data. Can be a file path or bytes.
            text (Optional[str]): Caption for the music. Defaults to None.
            reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
            via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
            performer (Optional[str]): Name of the performer/artist. Defaults to None (auto-detect).
            time (Optional[int]): Custom duration for the music in seconds. Defaults to None (auto-detect).
            schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
                When to send the message.
                - Unix timestamp (int/float): Absolute time
                - timedelta: Relative time from now
                - datetime: Absolute date and time
            schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
            base64 (str, optional): Base64 encoded music data.

        Returns:
            The API response containing the sent message details.
        """
        if music is None and base64 is None:
            raise InvalidInput("Either 'music' or 'base64' must be provided.")

        if music is not None:
            base64 = None

        return await self.send_message(
            chat=chat,
            text=text,
            reply_to_message_id=reply_to_message_id,
            file_inline=music,
            type='Music',
            via_bot=via_bot,
            performer=performer,
            time=time,
            schedule_time=schedule_time,
            schedule_type=schedule_type,
            base64_data=base64,
            **kwargs
        )