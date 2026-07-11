from typing import Union, Optional
from pathlib import Path
import maxrubika

class SendVoice:
    async def send_voice(
        self: "maxrubika.Client",
        chat: str,
        voice: Union[Path, bytes],
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        time: Optional[int] = None,
        auto_delete: Optional[int] = None
    ):
        """
        Send a voice message to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            voice (Path, bytes): The voice data. Can be a file path or bytes.
            text (Optional[str]): Caption for the voice message. Defaults to None.
            reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
            is_spoil (bool): Whether the voice message should be marked as a spoiler. Defaults to False.
            via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
            time (Optional[int]): Custom duration for the voice message in seconds. Defaults to None (auto-detect).
            auto_delete (Optional[int]): Auto-delete duration in seconds. Defaults to None.

        Returns:
            The API response containing the sent message details.
        """
        return await self.send_message(
            chat=chat,
            text=text,
            reply_to_message_id=reply_to_message_id,
            file_inline=voice,
            type='Voice',
            via_bot=via_bot,
            time=time,
            auto_delete=auto_delete
        )