from typing import Union, Optional, Literal, TYPE_CHECKING
from pathlib import Path
from datetime import timedelta, datetime

if TYPE_CHECKING:
    import maxrubika
    from ....data import Data

class SendMusic:
    async def send_music(
        self: "maxrubika.Messenger",
        chat: str,
        music: Optional[Union[Path, str, bytes]] = None,
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        performer: Optional[str] = None,
        time: Optional[int] = None,
        is_mute: bool = False,
        metadata: Optional[dict] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
        base64: Optional[str] = None,
        file_inline: Optional[Union[dict, "Data"]] = None,
        **kwargs
    ):
        """
        Send a music file to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            music (Union[Path, str, bytes], optional): The music data (path, URL, or bytes).
            text (str, optional): Caption for the music (Max: 2048 chars, 64 lines).
            reply_to_message_id (Union[str, int], optional): ID of the message to reply to.
            via_bot (str, optional): Bot GUID or username to send the message via.
            performer (str, optional): Name of the performer/artist. Auto-detected if not provided.
            time (int, optional): Custom duration for the music in seconds. Auto-detected if not provided.
            is_mute (bool): If True, the message will be sent silently. Defaults to False.
            metadata (dict, optional): Pre-formatted metadata for the caption.
            schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
            schedule_type (str, optional): 'Default' or 'WhenOnline'.
            base64 (str, optional): Base64 encoded music data.
            file_inline (Union[dict, Data], optional): Pre-uploaded music object. If provided, 'music' and 'base64' are ignored.
            **kwargs: Additional parameters.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        if music is None and base64 is None and file_inline is None:
            raise InvalidInput("Either 'music', 'base64', or 'file_inline' must be provided.")

        return await self.send_file(
            chat=chat,
            file=music,
            text=text,
            type='Music',
            reply_to_message_id=reply_to_message_id,
            via_bot=via_bot,
            performer=performer,
            time=time,
            is_mute=is_mute,
            metadata=metadata,
            schedule_time=schedule_time,
            schedule_type=schedule_type,
            base64=base64,
            file_inline=file_inline,
            **kwargs
        )