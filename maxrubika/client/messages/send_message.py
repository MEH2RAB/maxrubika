from typing import Optional, Union, Literal
from pathlib import Path
from os import path
from datetime import timedelta, datetime
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
        auto_delete: Optional[Union[int, float]] = None,
        file_inline: Optional[Union[Data, Path, bytes]] = None,
        sticker: Optional[Union[Data, dict]] = None,
        type: str = 'File',
        is_spoil: bool = False,
        thumb: Optional[Union[bool, str]] = None,
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
            auto_delete (Optional[Union[int, float]]): Auto-delete duration in seconds.
            file_inline (Optional[Union[Data, Path, bytes]]): The file to attach.
            sticker (Optional[Union[Data, dict]]): Sticker data to attach.
            type (str): The type of file ('File', 'Image', 'Video', 'Gif', 'Music', 'Voice', 'VideoMessage').
            is_spoil (bool): Whether the media is a spoiler.
            thumb (Optional[Union[bool, str]]): Thumbnail - True for auto, str for base64, None for no thumbnail.
            audio_info (bool): Whether to extract audio metadata (Music/Voice only).
            metadata (Optional[dict]): Additional metadata for text formatting.
            performer (Optional[str]): Music performer name.
            schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
                When to send the message. Accepts:
                - Unix timestamp (int/float): Absolute time
                - timedelta: Relative time from now (e.g., timedelta(hours=1))
                - datetime: Absolute date and time
            schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
                'Default' uses schedule_time, 'WhenOnline' sends when user comes online (u0 only).
            **kwargs: Additional file metadata:
                - width (int): Custom width
                - height (int): Custom height
                - time (int): Custom duration in seconds
                - file_name (str): Custom file name

        Returns:
            The API response containing the sent message details.

        Note:
            - For Music, `time` is in **seconds**.
            - For Voice, Image, Gif, Video, VideoMessage, and File, `time` is in **milliseconds**.
            - If `schedule_time` is provided, `is_scheduled` is automatically set to True and `schedule_type` to 'Default'.
            - If `schedule_type='WhenOnline'` is provided, `is_scheduled` is automatically set to True.
              This only works for user chats (u0).
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

            file_inline = await self.upload_file(file_inline, file_name=kwargs.get('file_name'))

            if type == 'VideoMessage':
                file_inline['is_round'] = True
            file_inline['type'] = 'Video' if type == 'VideoMessage' else type

            if thumb_inline is not None:
                file_inline['thumb_inline'] = thumb_inline

            if custom_time is not None:
                file_inline['time'] = custom_time if type == 'Music' else custom_time * 1000
            elif type == 'Music' and audio_info_result is not None:
                file_inline['time'] = audio_info_result.duration
            elif thumb_obj is not None:
                file_inline['time'] = thumb_obj.seconds
            elif audio_info_result is not None:
                file_inline['time'] = audio_info_result.duration * 1000
            else:
                file_inline['time'] = 1 if type == 'Music' else 1000

            file_inline['width'] = custom_width or (thumb_obj.width if thumb_obj else 200)
            file_inline['height'] = custom_height or (thumb_obj.height if thumb_obj else 200)

            file_inline['music_performer'] = (
                custom_performer or
                (audio_info_result.performer if audio_info_result else '') if type == 'Music' else ''
            )

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