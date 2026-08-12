from typing import Union, Optional, Literal
from pathlib import Path
from datetime import timedelta, datetime
import maxrubika
from ..exceptions import InvalidInput

class SendGif:
    async def send_gif(
        self: "maxrubika.Client",
        chat: str,
        gif: Union[Path, bytes] = None,
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        thumb: Optional[Union[bool, str]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        time: Optional[int] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
        base64: str = None,
        **kwargs
    ):
        """
        Send a GIF to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            gif (Path, bytes, optional): The GIF data. Can be a file path or bytes.
            text (Optional[str]): Caption for the GIF. Defaults to None.
            reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
            via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
            thumb (Optional[Union[bool, str]]): Thumbnail behavior:
                - None or True: Auto-generate thumbnail using available libraries (default)
                - False: Use default thumbnail
                - str: Custom thumbnail as Base64 string (pure Base64, no data:image header)
            width (Optional[int]): Custom width for the GIF. Defaults to None (auto-detect).
            height (Optional[int]): Custom height for the GIF. Defaults to None (auto-detect).
            time (Optional[int]): Custom duration for the GIF in seconds. Defaults to None (auto-detect).
            schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
                When to send the message.
                - Unix timestamp (int/float): Absolute time
                - timedelta: Relative time from now
                - datetime: Absolute date and time
            schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
            base64 (str, optional): Base64 encoded GIF data.

        Returns:
            The API response containing the sent message details.
        """
        if gif is None and base64 is None:
            raise InvalidInput("Either 'gif' or 'base64' must be provided.")

        if gif is not None:
            base64 = None

        return await self.send_message(
            chat=chat,
            text=text,
            reply_to_message_id=reply_to_message_id,
            file_inline=gif,
            type='Gif',
            via_bot=via_bot,
            thumb=thumb,
            width=width,
            height=height,
            time=time,
            schedule_time=schedule_time,
            schedule_type=schedule_type,
            base64_data=base64,
            **kwargs
        )