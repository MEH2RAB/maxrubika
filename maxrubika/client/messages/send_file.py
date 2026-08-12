from typing import Optional, Union, Literal
from pathlib import Path
from datetime import timedelta, datetime
import maxrubika
from ..exceptions import InvalidInput

class SendFile:
    async def send_file(
        self: "maxrubika.Client",
        chat: str,
        file: Union[Path, bytes] = None,
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
        base64: str = None,
        **kwargs
    ):
        """
        Send a file.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            file (Union[Path, bytes], optional): The file data (path or bytes).
            text (Optional[str]): The caption for the file. Defaults to None.
            reply_to_message_id (Optional[Union[str, int]]): The ID of the message to which this is a reply. Defaults to None.
            via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
            schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
                When to send the message.
                - Unix timestamp (int/float): Absolute time
                - timedelta: Relative time from now
                - datetime: Absolute date and time
            schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
            base64 (str, optional): Base64 encoded file data.

        Returns:
            The result of the API call.
        """
        if file is None and base64 is None:
            raise InvalidInput("Either 'file' or 'base64' must be provided.")

        if file is not None:
            base64 = None

        return await self.send_message(
            chat=chat,
            text=text,
            reply_to_message_id=reply_to_message_id,
            file_inline=file,
            type='File',
            thumb=False,
            via_bot=via_bot,
            schedule_time=schedule_time,
            schedule_type=schedule_type,
            base64_data=base64,
            **kwargs
        )