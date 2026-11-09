from typing import Union, Optional, List, Literal, TYPE_CHECKING
from pathlib import Path
from os import path
import random

if TYPE_CHECKING:
    import maxrubika

class SendLive:
    async def send_live(
        self: "maxrubika.Messenger",
        chat: str,
        title: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        thumb: Optional[Union[str, Path, bytes]] = None,
        suggestion_comments: Optional[List[str]] = None,
        device_type: Literal['Software', 'Mobile'] = 'Software'
    ):
        """
        Send a live stream.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            title (str, optional): Live stream title.
            reply_to_message_id (Union[str, int], optional): The ID of the message to which this is a reply.
            thumb (Union[str, Path, bytes], optional): Thumbnail for the live stream. str (base64/path/URL), Path, or bytes. Default thumbnail if not provided.
            suggestion_comments (List[str], optional): Suggested comments for the live stream.
            device_type (str): The device type. 'Software' or 'Mobile'. Case-insensitive. Defaults to 'Software'.

        Returns:
            The result of the API call.
        """
        import aiohttp
        import aiofiles
        from ...core import media
        from ...exceptions import InvalidInput

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

        device_type_map = {
            'software': 'Software',
            'mobile': 'Mobile',
        }
        device_type = device_type_map.get(device_type.lower())

        if not device_type:
            raise InvalidInput("'device_type' must be 'Software' or 'Mobile'.")

        input_data = {
            'object_guid': chat_guid,
            'title': title,
            'device_type': device_type,
            'thumb_inline': thumb,
            'rnd': random.randint(100000, 999999),
            'reply_to_message_id': reply_to_message_id
        }

        if suggestion_comments is not None:
            input_data['suggestion_comments'] = suggestion_comments

        return await self.request(method='sendLive', input=input_data)