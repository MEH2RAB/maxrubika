from typing import Optional, Union
from pathlib import Path
import maxrubika

class SendVideoMessage:
    async def send_video_message(
        self: "maxrubika.Client",
        chat: str,
        video_message: Union[Path, bytes],
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        is_spoil: bool = False,
        via_bot: Optional[str] = None,
        thumb: Optional[Union[bool, str]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        time: Optional[int] = None,
        auto_delete: Optional[int] = None
    ):
        """
        Send a video message (round video) to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            video_message (Path, bytes): The video message data. Can be a file path or bytes.
            text (Optional[str]): Caption for the video message. Defaults to None.
            reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
            is_spoil (bool): Whether the video message should be marked as a spoiler. Defaults to False.
            via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
            thumb (Optional[Union[bool, str]]): Thumbnail behavior:
                - None or True: Auto-generate thumbnail using available libraries (or default).
                - str: Custom thumbnail as Base64 string.
            width (Optional[int]): Custom width for the video message. Defaults to None (auto-detect).
            height (Optional[int]): Custom height for the video message. Defaults to None (auto-detect).
            time (Optional[int]): Custom duration for the video message in seconds. Defaults to None (auto-detect).
            auto_delete (Optional[int]): Auto-delete duration in seconds. Defaults to None.

        Returns:
            The API response containing the sent message details.
        """
        return await self.send_message(
            chat=chat,
            text=text,
            reply_to_message_id=reply_to_message_id,
            file_inline=video_message,
            is_spoil=is_spoil,
            type='VideoMessage',
            via_bot=via_bot,
            thumb=thumb,
            width=width,
            height=height,
            time=time,
            auto_delete=auto_delete,
        )