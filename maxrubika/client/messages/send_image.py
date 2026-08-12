from typing import Union, Optional, Literal
from pathlib import Path
from datetime import timedelta, datetime
import maxrubika
from ..exceptions import InvalidInput

class SendImage:
    async def send_image(
        self: "maxrubika.Client",
        chat: str,
        image: Union[Path, bytes] = None,
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        is_spoil: bool = False,
        via_bot: Optional[str] = None,
        thumb: Optional[Union[bool, str]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
        base64: str = None,
        **kwargs
    ):
        """
        Send an image to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            image (Path, bytes, optional): The image data. Can be a file path or bytes.
            text (Optional[str]): Caption for the image. Defaults to None.
            reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
            is_spoil (bool): Whether the image should be marked as a spoiler. Defaults to False.
            via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
            thumb (Optional[Union[bool, str]]): Thumbnail behavior:
                - None or True: Auto-generate thumbnail using available libraries (or default).
                - str: Custom thumbnail as Base64 string.
            width (Optional[int]): Custom width for the image. Defaults to None (auto-detect).
            height (Optional[int]): Custom height for the image. Defaults to None (auto-detect).
            schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
                When to send the message.
                - Unix timestamp (int/float): Absolute time
                - timedelta: Relative time from now
                - datetime: Absolute date and time
            schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
            base64 (str, optional): Base64 encoded image data.

        Returns:
            The API response containing the sent message details.
        """
        if image is None and base64 is None:
            raise InvalidInput("Either 'image' or 'base64' must be provided.")

        if image is not None:
            base64 = None

        return await self.send_message(
            chat=chat,
            text=text,
            reply_to_message_id=reply_to_message_id,
            file_inline=image,
            is_spoil=is_spoil,
            type='Image',
            thumb=thumb,
            via_bot=via_bot,
            width=width,
            height=height,
            schedule_time=schedule_time,
            schedule_type=schedule_type,
            base64_data=base64,
            **kwargs
        )