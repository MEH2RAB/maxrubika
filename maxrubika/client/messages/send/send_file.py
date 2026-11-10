from typing import Optional, Union, Literal, TYPE_CHECKING
from pathlib import Path
from os import path
from datetime import timedelta, datetime
import base64 as b64lib
import random
import mimetypes
import time as time_module

if TYPE_CHECKING:
    import maxrubika
    from ....data import Data

async def get_mime_from_url(session, url: str):
    async with session.head(url) as response:
        content_type = response.content_type
        if content_type:
            return mimetypes.guess_extension(content_type.split(';')[0])

class SendFile:
    async def send_file(
        self: "maxrubika.Messenger",
        chat: str,
        file: Optional[Union[Path, str, bytes, "Data"]] = None,
        text: Optional[str] = None,
        type: str = 'File',
        is_spoil: bool = False,
        thumb: Optional[Union[bool, str, Path, bytes]] = None,
        audio_info: bool = True,
        performer: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        is_mute: bool = False,
        metadata: Optional[dict] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[Literal['Default', 'WhenOnline']] = None,
        base64: Optional[str] = None,
        file_inline: Optional[Union[dict, "Data"]] = None,
        **kwargs
    ):
        """
        Send a file (Image, Video, Voice, Music, Gif, File) to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat. Use 'me', 'cloud', 'self', or 'myself' for saved messages.
            file (Union[Path, str, bytes, Data], optional): The file data (path, URL, bytes, or Data object).
            text (str, optional): The caption for the file (Max: 2048 chars, 64 lines).
            type (str): The type of the file ('File', 'Image', 'Video', 'Voice', 'Music', 'Gif', 'VideoMessage'). Defaults to 'File'.
            is_spoil (bool): If True, the file will be marked as spoil.
            thumb (Union[bool, str, Path, bytes], optional): Thumbnail for the file.
            audio_info (bool): If True, extracts audio info for Music/Voice.
            performer (str, optional): Music performer name.
            reply_to_message_id (Union[str, int], optional): The ID of the message to which this is a reply.
            via_bot (str, optional): Bot GUID or username to send the message via.
            is_mute (bool): If True, the message will be sent silently.
            metadata (dict, optional): Pre-formatted metadata for the caption.
            schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
            schedule_type (str, optional): 'Default' or 'WhenOnline'.
            base64 (str, optional): Base64 encoded file data.
            file_inline (Union[dict, Data], optional): Pre-uploaded file object. If provided, 'file' and 'base64' are ignored.
            **kwargs: Additional parameters (e.g., file_name, width, height, time, callback).

        Returns:
            The result of the API call.
        """
        import aiohttp, aiofiles
        from ....data import Data
        from ...core import media, to_metadata
        from ...exceptions import InvalidInput, MessageTooLong

        if text is not None:
            if not isinstance(text, str):
                raise InvalidInput("'text' must be a string.")
            if len(text) > 2048:
                message = f"Caption is too long ({len(text)} characters). Maximum allowed is 2048."
                raise MessageTooLong(message)
            if text.count('\n') > 64:
                message = f"Caption has too many lines ({text.count(chr(10))}). Maximum allowed is 64."
                raise MessageTooLong(message)

        if file is None and base64 is None and file_inline is None:
            raise InvalidInput("Either 'file', 'base64', or 'file_inline' must be provided.")

        if base64:
            try:
                file = b64lib.b64decode(base64)
            except Exception:
                raise InvalidInput("Invalid base64 data.") from None

        if file is not None and file_inline is None:
            if isinstance(file, (str, Path)):
                file_str = str(file)
                if not (file_str.startswith(('http://', 'https://')) or path.exists(file_str)):

                    message = f"File not found: {file_str}\nPlease check if the file path is correct, or provide the file as bytes, URL, base64, or file_inline."
                    raise FileNotFoundError(message)
            elif not isinstance(file, (bytes, Data, dict)):
                message = f"Unsupported 'file' type: {type(file).__name__}. Expected a path (str/Path), URL, bytes, Data, or dict."
                raise InvalidInput(message)

        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        input_data = {
            'object_guid': chat_guid,
            'reply_to_message_id': reply_to_message_id,
            'rnd': random.randint(100000, 999999)
        }

        if is_mute:
            input_data['is_mute'] = True

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
                message = f"Invalid schedule_time type: {type(schedule_time).__name__}"
                raise InvalidInput(message)

            if schedule_time <= time_module.time():
                raise InvalidInput("'schedule_time' must be in the future.")

            input_data['is_scheduled'] = True
            input_data['schedule_type'] = 'Default'
            input_data['scheduled_time'] = schedule_time

        elif schedule_type is not None:
            if schedule_type == 'WhenOnline':
                if not chat_guid.startswith('u0'):
                    raise InvalidInput("'schedule_type=WhenOnline' is only available for user chats.")
                input_data['is_scheduled'] = True
                input_data['schedule_type'] = 'WhenOnline'
            elif schedule_type == 'Default':
                raise InvalidInput("'schedule_type=Default' requires 'schedule_time'.")

        if via_bot is not None:
            bot_guid = await self.get_guid(via_bot)
            if not bot_guid.startswith('b0'):
                message = f"'{via_bot}' does not point to a valid bot. Expected a bot GUID or bot username."
                raise InvalidInput(message)
            input_data['via_bot_guid'] = bot_guid

        if text:
            processed_text = text
            if not metadata:
                try:
                    processed = to_metadata(text)
                    processed_text = processed['text']
                    metadata = processed.get('metadata')
                except Exception:
                    processed_text = text
                    metadata = None

            input_data['text'] = processed_text.strip()

            if metadata:
                if 'metadata' in metadata:
                    input_data.update(metadata)
                else:
                    input_data['metadata'] = metadata

        if file_inline is not None:
            if isinstance(file_inline, Data):
                input_data['file_inline'] = file_inline.original_data
            elif isinstance(file_inline, dict):
                input_data['file_inline'] = file_inline
            else:
                raise InvalidInput("'file_inline' must be a dict or Data object.")

            return await self.request(method='sendMessage', input=input_data)

        if file is not None:
            if isinstance(file, (str, Path)):
                if str(file).startswith(('http://', 'https://')):
                    async with aiohttp.ClientSession(headers={'user-agent': self.user_agent}) as cs:
                        mime = await get_mime_from_url(session=cs, url=str(file))
                        kwargs['file_name'] = kwargs.get('file_name', ''.join([str(input_data['rnd']), mime or f'.{type}']))
                        async with cs.get(str(file)) as result:
                            file = await result.read()
                elif path.exists(str(file)):
                    async with aiofiles.open(str(file), 'rb') as f:
                        kwargs['file_name'] = kwargs.get('file_name', path.basename(str(file)))
                        file = await f.read()

            if isinstance(file, bytes):
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
                    audio_info_result = media.Audio.get_audio_info(file)
                    if isinstance(audio_info_result, media.AudioResult):
                        if custom_performer is None and type == 'Music':
                            custom_performer = audio_info_result.performer

                thumb_obj = None
                if type == 'Image':
                    thumb_obj = media.MediaThumbnail.from_image(file)
                elif type in ('Video', 'Gif', 'VideoMessage'):
                    thumb_obj = media.MediaThumbnail.from_video(file)

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

                file_inline_data = await self.upload_file(
                    file=file,
                    file_name=kwargs.get('file_name'),
                    callback=kwargs.get('callback'))

                if type == 'VideoMessage':
                    file_inline_data['is_round'] = True
                file_inline_data['type'] = 'Video' if type == 'VideoMessage' else type

                if thumb_inline is not None:
                    file_inline_data['thumb_inline'] = thumb_inline

                if custom_time is not None:
                    custom_time = int(custom_time)
                    file_inline_data['time'] = custom_time if type == 'Music' else custom_time * 1000
                elif type == 'Music' and audio_info_result is not None:
                    file_inline_data['time'] = audio_info_result.duration
                elif isinstance(thumb_obj, media.ResultMedia):
                    file_inline_data['time'] = thumb_obj.seconds
                elif audio_info_result is not None:
                    file_inline_data['time'] = audio_info_result.duration * 1000
                else:
                    file_inline_data['time'] = 1 if type == 'Music' else 1000

                file_inline_data['width'] = custom_width or (thumb_obj.width if isinstance(thumb_obj, media.ResultMedia) else 200)
                file_inline_data['height'] = custom_height or (thumb_obj.height if isinstance(thumb_obj, media.ResultMedia) else 200)

                file_inline_data['music_performer'] = (
                    custom_performer or
                    (audio_info_result.performer if audio_info_result else '') if type == 'Music' else ''
                )

                file_inline_data['is_spoil'] = bool(is_spoil)

                input_data['file_inline'] = file_inline_data if isinstance(file_inline_data, dict) else file_inline_data.to_dict()

            elif isinstance(file, (Data, dict)):
                input_data['file_inline'] = file.original_data if isinstance(file, Data) else file

        return await self.request(method='sendMessage', input=input_data)