from typing import Union, Optional
from pathlib import Path
from os import path
import random
import aiohttp
import aiofiles
import maxrubika
from ..core import media

class SendLive:
    async def send_live(
        self: "maxrubika.Client",
        chat: str,
        title: str = None,
        reply_to_message_id: Union[str, int] = None,
        thumb: Optional[Union[str, Path, bytes]] = None
    ):
        """
        Send a live stream.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            title (str): Live stream title.
            reply_to_message_id (Optional[Union[str, int]]): The ID of the message to which this is a reply. Defaults to None.
            thumb (Optional[Union[str, Path, bytes]]): Thumbnail for the live stream.
                - str: Base64 encoded string, file path, or URL.
                - Path: Path to thumbnail file.
                - bytes: Raw thumbnail bytes.
                If not provided, a default thumbnail will be used.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if thumb is None:
            thumb = media.MediaThumbnail._default_thumbnail()
        elif isinstance(thumb, bytes):
            result = media.MediaThumbnail.from_manual(thumb)
            thumb = result.to_base64() if isinstance(result, media.ResultMedia) else result
        elif isinstance(thumb, (str, Path)):
            thumb_data = None
            if isinstance(thumb, Path) or (isinstance(thumb, str) and path.exists(thumb)):
                if isinstance(thumb, str):
                    async with aiofiles.open(thumb, 'rb') as f:
                        thumb_data = await f.read()
                else:
                    async with aiofiles.open(str(thumb), 'rb') as f:
                        thumb_data = await f.read()
            elif isinstance(thumb, str) and thumb.startswith('http'):
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(thumb) as resp:
                        thumb_data = await resp.read()

            if thumb_data:
                result = media.MediaThumbnail.from_manual(thumb_data)
                thumb = result.to_base64() if isinstance(result, media.ResultMedia) else result

        return await self.request(
            method='sendLive',
            input={
                'object_guid': chat_guid,
                'title': title,
                'device_type': 'Software',
                'thumb_inline': thumb,
                'rnd': random.randint(100000, 999999),
                'reply_to_message_id': reply_to_message_id
            }
        )