from typing import Union, Optional, Literal, TYPE_CHECKING
from pathlib import Path
from datetime import timedelta, datetime

if TYPE_CHECKING:
    import maxrubika
    from ....data import Data

class SendImage:
    async def send_image(
        self: "maxrubika.Messenger",
        chat: str,
        image: Optional[Union[Path, str, bytes]] = None,
        file_inline: Optional[Union[dict, "Data"]] = None,
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        is_spoil: bool = False,
        via_bot: Optional[str] = None,
        thumb: Optional[Union[bool, str]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        is_mute: bool = False,
        metadata: Optional[dict] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
        base64: Optional[str] = None,
        **kwargs
    ):
        """
        Send an image to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            image (Union[Path, str, bytes], optional): The image data (path, URL, or bytes).
            file_inline (Union[dict, Data], optional): Pre-uploaded image object. If provided, 'image' and 'base64' are ignored.
            text (str, optional): Caption for the image (Max: 2048 chars, 64 lines).
            reply_to_message_id (Union[str, int], optional): ID of the message to reply to.
            is_spoil (bool): Whether the image should be marked as a spoiler. Defaults to False.
            via_bot (str, optional): Bot GUID or username to send the message via.
            thumb (Union[bool, str], optional): Thumbnail behavior.
            width (int, optional): Custom width for the image.
            height (int, optional): Custom height for the image.
            is_mute (bool): If True, the message will be sent silently. Defaults to False.
            metadata (dict, optional): Pre-formatted metadata for the caption.
            schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
            schedule_type (str, optional): 'Default' or 'WhenOnline'.
            base64 (str, optional): Base64 encoded image data.
            **kwargs: Additional parameters.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        if image is None and base64 is None and file_inline is None:
            raise InvalidInput("Either 'image', 'base64', or 'file_inline' must be provided.")

        return await self.send_file(
            chat=chat,
            file=image,
            file_inline=file_inline,
            text=text,
            type='Image',
            is_spoil=is_spoil,
            reply_to_message_id=reply_to_message_id,
            via_bot=via_bot,
            thumb=thumb,
            width=width,
            height=height,
            is_mute=is_mute,
            metadata=metadata,
            schedule_time=schedule_time,
            schedule_type=schedule_type,
            base64=base64,
            **kwargs
        )