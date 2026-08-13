from typing import Optional, Union, Literal
from pathlib import Path
from os import path
from datetime import timedelta, datetime
import base64
import random
import aiohttp
import aiofiles
import mimetypes
import asyncio
import time as time_module
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
        file_inline: Optional[Union[Data, Path, bytes]] = None,
        base64_data: Optional[str] = None,
        sticker: Optional[Union[Data, dict]] = None,
        type: str = 'File',
        is_spoil: bool = False,
        thumb: Optional[Union[bool, str, Path, bytes]] = None,
        audio_info: bool = True,
        metadata: Optional[dict] = None,
        performer: Optional[str] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
        **kwargs
    ):
        """
        Send a message to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            text (Optional[str]): The text content of the message.
            reply_to_message_id (Optional[Union[str, int]]): The ID of the message to reply to.
            via_bot (Optional[str]): Bot GUID or username to send the message via.
            metadata (Optional[dict]): Additional metadata for text formatting.
            schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
                When to send the message. Accepts:
                - Unix timestamp (int/float): Absolute time
                - timedelta: Relative time from now (e.g., timedelta(hours=1))
                - datetime: Absolute date and time
            schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online.

        Returns:
            The API response containing the sent message details.

        Note:
            - If `schedule_time` is provided, `is_scheduled` is automatically set to True and `schedule_type` to 'Default'.
            - If `schedule_type='WhenOnline'` is provided, `is_scheduled` is automatically set to True.
              This only works for user chats.
        """
        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        input = {
            'object_guid': chat_guid,
            'reply_to_message_id': reply_to_message_id,
            'rnd': random.randint(100000, 999999)
        }

        if schedule_time is not None:
            if isinstance(schedule_time, timedelta):
                schedule_time = int(time_module.time() + schedule_time.total_seconds())
            elif isinstance(schedule_time, datetime):
                schedule_time = int(schedule_time.timestamp())
            elif isinstance(schedule_time, (int, float)):
                if schedule_time < 1000000000:
                    schedule_time = int(time_module.time() + schedule_time)
                else:
                    schedule_time = int(schedule_time)
            else:
                raise InvalidInput(
                f"Invalid schedule_time type: {type(schedule_time).__name__}")

            if schedule_time <= time_module.time():
                raise InvalidInput("'schedule_time' must be in the future.")

            input['is_scheduled'] = True
            input['schedule_type'] = 'Default'
            input['scheduled_time'] = schedule_time

        elif schedule_type is not None:
            if schedule_type == 'WhenOnline':
                if not chat_guid.startswith('u0'):
                    raise InvalidInput(
                        "'schedule_type=WhenOnline' is only available for user chats (private messages)."
                    )
                input['is_scheduled'] = True
                input['schedule_type'] = 'WhenOnline'
            elif schedule_type == 'Default':
                raise InvalidInput(
                    "'schedule_type=Default' requires 'schedule_time' to be provided."
                )

        if via_bot is not None:
            bot_guid = await self.get_guid(via_bot)
            if not bot_guid.startswith('b0'):
                raise InvalidInput(f"'{via_bot}' does not point to a valid bot. Expected a bot GUID or bot username.")
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

        if base64_data:
            try:
                file_inline = base64.b64decode(base64_data)
            except Exception:
                raise InvalidInput("Invalid base64 data.")

        if file_inline is not None and isinstance(file_inline, str):
            if isinstance(file_inline, str):
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

            if isinstance(custom_time, timedelta):
                custom_time = custom_time.total_seconds()
            elif isinstance(custom_time, (int, float)):
                if custom_time >= 1000:
                    custom_time = custom_time / 1000

            audio_info_result = None
            if type in ('Music', 'Voice') and audio_info is True:
                audio_info_result = media.Audio.get_audio_info(file_inline)
                if isinstance(audio_info_result, media.AudioResult):
                    if custom_performer is None and type == 'Music':
                        custom_performer = audio_info_result.performer

            thumb_obj = None
            if type == 'Image':
                thumb_obj = media.MediaThumbnail.from_image(file_inline)
            elif type in ('Video', 'Gif', 'VideoMessage'):
                thumb_obj = media.MediaThumbnail.from_video(file_inline)

            NEEDS_THUMBNAIL = ('Image', 'Gif', 'Video', 'VideoMessage')
            use_thumb = True if (thumb is None and type in NEEDS_THUMBNAIL) else (False if thumb is None else thumb)

            thumb_inline = None

            if use_thumb is True:
                if isinstance(thumb_obj, media.ResultMedia):
                    thumb_inline = thumb_obj.to_base64()
                elif isinstance(thumb_obj, str):
                    thumb_inline = thumb_obj
            elif isinstance(use_thumb, bytes):
                result = media.MediaThumbnail.from_manual(use_thumb)
                if isinstance(result, media.ResultMedia):
                    thumb_inline = result.to_base64()
                else:
                    thumb_inline = result
            elif isinstance(use_thumb, (str, Path)):
                thumb_data = None
                if isinstance(use_thumb, Path) or (isinstance(use_thumb, str) and path.exists(use_thumb)):
                    if isinstance(use_thumb, str):
                        async with aiofiles.open(use_thumb, 'rb') as f:
                            thumb_data = await f.read()
                    else:
                        async with aiofiles.open(str(use_thumb), 'rb') as f:
                            thumb_data = await f.read()
                elif isinstance(use_thumb, str) and use_thumb.startswith('http'):
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(use_thumb) as resp:
                            thumb_data = await resp.read()
                else:
                    thumb_inline = use_thumb

                if thumb_data:
                    result = media.MediaThumbnail.from_manual(thumb_data)
                    if isinstance(result, media.ResultMedia):
                        thumb_inline = result.to_base64()
                    else:
                        thumb_inline = result

            file_inline = await self.upload_file(
                file=file_inline,
                file_name=kwargs.get('file_name'),
                callback=kwargs.get('callback'))

            if type == 'VideoMessage':
                file_inline['is_round'] = True
            file_inline['type'] = 'Video' if type == 'VideoMessage' else type

            if thumb_inline is not None:
                file_inline['thumb_inline'] = thumb_inline

            if custom_time is not None:
                custom_time = int(custom_time)
                file_inline['time'] = custom_time if type == 'Music' else custom_time * 1000
            elif type == 'Music' and audio_info_result is not None:
                file_inline['time'] = audio_info_result.duration
            elif isinstance(thumb_obj, media.ResultMedia):
                file_inline['time'] = thumb_obj.seconds
            elif audio_info_result is not None:
                file_inline['time'] = audio_info_result.duration * 1000
            else:
                file_inline['time'] = 1 if type == 'Music' else 1000

            file_inline['width'] = custom_width or (thumb_obj.width if isinstance(thumb_obj, media.ResultMedia) else 200)
            file_inline['height'] = custom_height or (thumb_obj.height if isinstance(thumb_obj, media.ResultMedia) else 200)

            file_inline['music_performer'] = (
                custom_performer or
                (audio_info_result.performer if audio_info_result else '') if type == 'Music' else ''
            )

            file_inline['is_spoil'] = bool(is_spoil)

        if file_inline is not None:
            input['file_inline'] = file_inline if isinstance(file_inline, dict) else file_inline.to_dict()
            result = await self.request(method = 'sendMessage', input = input)
        else:
            if 'text' in input:
                chunks = [input['text'][i:i+4200] for i in range(0, len(input['text']), 4200)]
                if not chunks:
                    result = await self.request(method = 'sendMessage', input = input)
                else:
                    for chunk in chunks:
                        input['text'] = chunk.strip()
                        result = await self.request(method = 'sendMessage', input = input)

        return result