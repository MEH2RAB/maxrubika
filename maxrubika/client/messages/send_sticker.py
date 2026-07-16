from typing import Optional, Union, Literal
from datetime import timedelta, datetime
import maxrubika

class SendSticker:
    async def send_sticker(
        self: "maxrubika.Client",
        chat: str,
        emoji_character: str,
        sticker_id: str,
        sticker_set_id: str,
        file: dict,
        w_h_ratio: str = '1.0',
        reply_to_message_id: Optional[Union[str, int]] = None,
        auto_delete: Optional[Union[str, float]] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None
    ):
        """
        Send a sticker.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            emoji_character (str): The emoji character associated with the sticker.
            sticker_id (str): The ID of the sticker.
            sticker_set_id (str): The ID of the sticker set.
            file (dict): The file data for the sticker.
            w_h_ratio (str): The width-to-height ratio of the sticker. Defaults to '1.0'.
            reply_to_message_id (Optional[Union[str, int]]): The ID of the message to which this is a reply. Defaults to None.
            auto_delete (Optional[Union[str, float]]): Auto-delete duration in seconds. Defaults to None.
            schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
                When to send the message.
                - Unix timestamp (int/float): Absolute time
                - timedelta: Relative time from now
                - datetime: Absolute date and time
            schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
        """
        if not isinstance(file, dict):
            file = file.to_dict()

        data = {
            'emoji_character': emoji_character,
            'sticker_id': sticker_id,
            'sticker_set_id': sticker_set_id,
            'w_h_ratio': w_h_ratio,
            'file': file,
        }

        return await self.send_message(
            chat=chat,
            sticker=data,
            reply_to_message_id=reply_to_message_id,
            auto_delete=auto_delete,
            schedule_time=schedule_time,
            schedule_type=schedule_type
        )