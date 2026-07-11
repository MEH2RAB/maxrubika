from typing import Union, Optional
from pathlib import Path
import maxrubika

class SendGif:
    async def send_gif(
        self: "maxrubika.Client",
        chat: str,
        gif: Union[Path, bytes],
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        thumb: Optional[Union[bool, str]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        time: Optional[int] = None,
        auto_delete: Optional[int] = None
    ):
        """
        Send a GIF to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            gif (Path, bytes): The GIF data. Can be a file path or bytes.
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
            auto_delete (Optional[int]): Auto-delete duration in seconds. Defaults to None.

        Returns:
            The API response containing the sent message details.
        """
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
            auto_delete=auto_delete,
        )