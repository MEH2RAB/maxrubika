from typing import Optional, Union
from pathlib import Path
from os import path
import random
import aiohttp
import aiofiles
import mimetypes
import asyncio
import maxrubika
from ...data import Data
from ..core import media
from ..core import to_metadata
from ..exceptions import InvalidInput

async def get_mime_from_url(session: "aiohttp.ClientSession", url: str):

    async with session.head(url) as response:
        content_type = response.content_type
        if content_type:
            return mimetypes.guess_extension(content_type.split(';')[0])

class SendMessage:
    async def send_message(
        self: "maxrubika.Client",
        chat: str,
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        auto_delete: Optional[Union[int, float]] = None,
        file_inline: Optional[Union[Data, Path, bytes]] = None,
        sticker: Optional[Union[Data, dict]] = None,
        type: str = 'File',
        is_spoil: bool = False,
        thumb: Optional[Union[bool, str]] = None,
        audio_info: bool = True,
        metadata: Optional[dict] = None,
        performer: Optional[str] = None,
        *args, **kwargs
    ):
        """
        Send a message to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            text (Optional[str]): The text content of the message.
            reply_to_message_id (Optional[Union[str, int]]): The ID of the message to reply to.
            via_bot (Optional[str]): Bot GUID or username to send the message via.
            auto_delete (Optional[Union[int, float]]): Auto-delete duration in seconds.

        Returns:
            The API response containing the sent message details.
        """
        if chat.lower() in ('me', 'cloud', 'self'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        input = {
            'object_guid': chat_guid,
            'reply_to_message_id': reply_to_message_id,
            'rnd': random.randint(100000, 999999)
        }

        if via_bot is not None:
            bot_guid = await self.get_guid(via_bot)
            if not bot_guid.startswith('b0'):
                raise InvalidInput(f"'{via_bot}' does not point to a valid bot.")
            input['via_bot_guid'] = bot_guid

        if text is not None and isinstance(text, str) and text.strip():
            processed_text = text
            if not metadata:
                try:
                    processed = to_metadata(text)
                    processed_text = processed['text']
                    metadata = processed.get('metadata')
                except Exception:
                    processed_text = text
                    metadata = None
            
            input['text'] = processed_text.strip()
            
            if metadata:
                if 'metadata' in metadata:
                    input.update(metadata)
                else:
                    input['metadata'] = metadata

        if isinstance(sticker, (Data, dict)):
            input['sticker'] = (
                sticker.original_data
                if isinstance(sticker, Data)
                else sticker
            )

        if file_inline is not None and isinstance(file_inline, str):
            if not file_inline.startswith('http'):
                async with aiofiles.open(file_inline, 'rb') as file:
                    kwargs['file_name'] = kwargs.get('file_name', path.basename(file_inline))
                    file_inline = await file.read()
            else:
                async with aiohttp.ClientSession(headers={'user-agent': self.user_agent}) as cs:
                    mime = await get_mime_from_url(session=cs, url=file_inline)
                    kwargs['file_name'] = kwargs.get('file_name', ''.join([str(input['rnd']), mime or f'.{type}']))
                    async with cs.get(file_inline) as result:
                        file_inline = await result.read()

        if isinstance(file_inline, bytes):
            custom_width = kwargs.get('width')
            custom_height = kwargs.get('height')
            custom_time = kwargs.get('time')
            custom_performer = performer

            audio_info_result = None
            if type in ('Music', 'Voice') and audio_info is True:
                audio_info_result = media.Audio.get_audio_info(file_inline)
                if isinstance(audio_info_result, media.AudioResult):
                    if custom_time is None:
                        custom_time = audio_info_result.duration
                    if custom_performer is None and type == 'Music':
                        custom_performer = audio_info_result.performer

            NEEDS_THUMBNAIL = ('Image', 'Gif', 'Video', 'VideoMessage')
            thumb = True if (thumb is None and type in NEEDS_THUMBNAIL) else (False if thumb is None else thumb)
            
            thumb_obj = None
            thumb_inline = None

            if thumb is True:
                if type == 'Image':
                    thumb_obj = media.MediaThumbnail.from_image(file_inline)
                elif type in ('Video', 'Gif', 'VideoMessage'):
                    thumb_obj = media.MediaThumbnail.from_video(file_inline)
                
                if isinstance(thumb_obj, media.ResultMedia):
                    thumb_inline = thumb_obj.to_base64()
                elif isinstance(thumb_obj, str):
                    thumb_inline = thumb_obj
            elif isinstance(thumb, str):
                thumb_inline = thumb

            file_inline = await self.upload_file(file_inline, *args, **kwargs)

            if type == 'VideoMessage':
                file_inline['is_round'] = True
            file_inline['type'] = 'Video' if type == 'VideoMessage' else type

            if thumb_inline is not None:
                file_inline['thumb_inline'] = thumb_inline

            if type == 'Music':
                if custom_time is not None:
                    file_inline['time'] = custom_time
                elif isinstance(audio_info_result, media.AudioResult):
                    file_inline['time'] = audio_info_result.duration
                else:
                    file_inline['time'] = 1

            else:
                if custom_time is not None:
                    file_inline['time'] = custom_time * 1000
                elif isinstance(thumb_obj, media.ResultMedia):
                    file_inline['time'] = thumb_obj.seconds
                elif isinstance(audio_info_result, media.AudioResult):
                    file_inline['time'] = audio_info_result.duration * 1000
                else:
                    file_inline['time'] = 1000

            if custom_width is not None:
                file_inline['width'] = custom_width
            elif isinstance(thumb_obj, media.ResultMedia):
                file_inline['width'] = thumb_obj.width
            else:
                file_inline['width'] = 200

            if custom_height is not None:
                file_inline['height'] = custom_height
            elif isinstance(thumb_obj, media.ResultMedia):
                file_inline['height'] = thumb_obj.height
            else:
                file_inline['height'] = 200

            if type == 'Music':
                if custom_performer:
                    file_inline['music_performer'] = custom_performer
                elif isinstance(audio_info_result, media.AudioResult):
                    file_inline['music_performer'] = audio_info_result.performer
                else:
                    file_inline['music_performer'] = ''
            else:
                file_inline['music_performer'] = ''

            file_inline['is_spoil'] = bool(is_spoil)

        if file_inline is not None:
            input['file_inline'] = file_inline if isinstance(file_inline, dict) else file_inline.to_dict()
            result = await self.request('sendMessage', input=input)
        else:
            if 'text' in input:
                chunks = [input['text'][i:i+4200] for i in range(0, len(input['text']), 4200)]
                if not chunks:
                    result = await self.request('sendMessage', input=input)
                else:
                    for chunk in chunks:
                        input['text'] = chunk.strip()
                        result = await self.request('sendMessage', input=input)

        if isinstance(auto_delete, (int, float)):
            asyncio.create_task(self.auto_delete_message(result.object_guid, result.message_id, auto_delete))

        return result