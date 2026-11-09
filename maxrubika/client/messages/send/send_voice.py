from typing import Union, Optional, Literal, TYPE_CHECKING
from pathlib import Path
from datetime import timedelta, datetime

if TYPE_CHECKING:
    import maxrubika
    from ...data import Data

class SendVoice:
    async def send_voice(
        self: "maxrubika.Messenger",
        chat: str,
        voice: Optional[Union[Path, str, bytes]] = None,
        file_inline: Optional[Union[dict, "Data"]] = None,
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        time: Optional[int] = None,
        is_mute: bool = False,
        metadata: Optional[dict] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
        base64: Optional[str] = None,
        **kwargs
    ):
        """
        Send a voice message to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            voice (Union[Path, str, bytes], optional): The voice data (path, URL, or bytes).
            file_inline (Union[dict, Data], optional): Pre-uploaded voice object. If provided, 'voice' and 'base64' are ignored.
            text (str, optional): Caption for the voice message (Max: 2048 chars, 64 lines).
            reply_to_message_id (Union[str, int], optional): ID of the message to reply to.
            via_bot (str, optional): Bot GUID or username to send the message via.
            time (int, optional): Custom duration for the voice message in seconds. Auto-detected if not provided.
            is_mute (bool): If True, the message will be sent silently. Defaults to False.
            metadata (dict, optional): Pre-formatted metadata for the caption.
            schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
            schedule_type (str, optional): 'Default' or 'WhenOnline'.
            base64 (str, optional): Base64 encoded voice data.
            **kwargs: Additional parameters.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        if voice is None and base64 is None and file_inline is None:
            raise InvalidInput("Either 'voice', 'base64', or 'file_inline' must be provided.")

        return await self.send_file(
            chat=chat,
            file=voice,
            file_inline=file_inline,
            text=text,
            type='Voice',
            reply_to_message_id=reply_to_message_id,
            via_bot=via_bot,
            time=time,
            is_mute=is_mute,
            metadata=metadata,
            schedule_time=schedule_time,
            schedule_type=schedule_type,
            base64=base64,
            **kwargs
        )