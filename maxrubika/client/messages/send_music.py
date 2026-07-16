from typing import Union, Optional, Literal
from pathlib import Path
from datetime import timedelta, datetime
import maxrubika

class SendMusic:
    async def send_music(
        self: "maxrubika.Client",
        chat: str,
        music: Union[Path, bytes],
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        performer: Optional[str] = None,
        time: Optional[int] = None,
        auto_delete: Optional[int] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None
    ):
        """
        Send a music file to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            music (Path, bytes): The music data. Can be a file path or bytes.
            text (Optional[str]): Caption for the music. Defaults to None.
            reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
            via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
            performer (Optional[str]): Name of the performer/artist. Defaults to None (auto-detect).
            time (Optional[int]): Custom duration for the music in seconds. Defaults to None (auto-detect).
            auto_delete (Optional[int]): Auto-delete duration in seconds. Defaults to None.
            schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
                When to send the message.
                - Unix timestamp (int/float): Absolute time
                - timedelta: Relative time from now
                - datetime: Absolute date and time
            schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).

        Returns:
            The API response containing the sent message details.
        """
        return await self.send_message(
            chat=chat,
            text=text,
            reply_to_message_id=reply_to_message_id,
            file_inline=music,
            type='Music',
            via_bot=via_bot,
            performer=performer,
            time=time,
            auto_delete=auto_delete,
            schedule_time=schedule_time,
            schedule_type=schedule_type
        )