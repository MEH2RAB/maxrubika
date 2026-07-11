from typing import Literal, Union
import maxrubika
from ..data import Data

class Event(Data):
    def __init__(self, event: dict, *args, **kwargs) -> None:
        super().__init__(event)
        self.client: "maxrubika.Client" = event.get("client")
        
        msg = event.get('message', {}) if isinstance(event.get('message'), dict) else {}
        fi = msg.get('file_inline', {}) if isinstance(msg.get('file_inline'), dict) else {}
        
        self.action = event.get('action', '')
        self.type = event.get('type', '')
        self.message_id = event.get('message_id', '')
        self.object_guid = event.get('object_guid', '')
        self.timestamp = event.get('timestamp', '')
        self.user_guid = event.get('user_guid', '')
        
        self.text = msg.get('text', '')
        self.is_edited = msg.get('is_edited', False)
        self.author_guid = msg.get('author_object_guid', '')
        self.reply_to_message_id = msg.get('reply_to_message_id', None)
        self.forwarded_from = msg.get('forwarded_from', None)
        self.forwarded_no_link = msg.get('forwarded_no_link', None)
        self.metadata = msg.get('metadata', None)
        self.reactions = msg.get('reactions', None)
        self.event_data = msg.get('event_data', None)
        self.message_type = msg.get('type', '')
        
        self.file_inline_raw = msg.get('file_inline', None)
        self.file_type = fi.get('type', '')
        self.is_round = fi.get('is_round', False)
        self.sticker_raw = msg.get('sticker', None)

        self.file_name = fi.get('file_name', '')
        self.file_size = fi.get('size', 0)
        self.file_dc_id = fi.get('dc_id', '')
        self.file_access_hash = fi.get('access_hash_rec', '')
        self.file_width = fi.get('width', 0)
        self.file_height = fi.get('height', 0)
        self.file_duration = fi.get('time', 0)
        self.file_mime = fi.get('mime', '')
        self.thumb_inline = fi.get('thumb_inline', '') if self.file_type in ('Image', 'Video', 'Gif', 'VideoMessage') else ''
        self.music_performer = fi.get('music_performer', '')
        
        self.user_activity_guid = event.get('user_activity_guid', '')
        self.object_type = event.get('object_type', '')
        self.updated_parameters = event.get('updated_parameters', [])

    @property
    def original_data(self):
        return self._data

    @property
    def chat_guid(self):
        return self.object_guid

    @property
    def is_me(self):
        return self.author_guid == self.client.guid if self.client else False

    @property
    def is_group(self):
        return self.object_guid.startswith('g0') if self.object_guid else False

    @property
    def is_channel(self):
        return self.object_guid.startswith('c0') if self.object_guid else False

    @property
    def is_pv(self):
        return self.object_guid.startswith('u0') if self.object_guid else False

    @property
    def is_bot(self):
        return self.object_guid.startswith('b0') if self.object_guid else False

    @property
    def is_service(self):
        return self.object_guid.startswith('s0') if self.object_guid else False

    @property
    def is_text(self):
        return self.message_type == 'Text'

    @property
    def is_event(self):
        return self.message_type == 'Event'

    @property
    def is_forward(self):
        return self.forwarded_from is not None

    @property
    def is_file_inline(self):
        return self.message_type in ['FileInline', 'FileInlineCaption']

    @property
    def is_reply(self):
        return bool(self.reply_to_message_id)

    @property
    def forward_type_from(self):
        return self.forwarded_from.get('type_from', None) if isinstance(self.forwarded_from, dict) else None

    @property
    def is_forwarded_from_user(self):
        return self.forward_type_from == 'User'

    @property
    def is_forwarded_from_channel(self):
        return self.forward_type_from == 'Channel'

    @property
    def is_forwarded_from_bot(self):
        return self.forward_type_from == 'Bot'

    @property
    def is_forwarded_no_link(self):
        return bool(self.forwarded_no_link)

    @property
    def file_inline(self):
        return Data(self.file_inline_raw) if isinstance(self.file_inline_raw, dict) else None

    @property
    def message(self):
        return Data(self._data.get('message', {})) if isinstance(self._data.get('message'), dict) else None

    @property
    def is_image(self):
        return self.file_type == 'Image'

    @property
    def is_video(self):
        return self.file_type == 'Video' and not self.is_round

    @property
    def is_video_message(self):
        return self.file_type == 'Video' and self.is_round

    @property
    def is_voice(self):
        return self.file_type == 'Voice'

    @property
    def is_music(self):
        return self.file_type == 'Music'

    @property
    def is_gif(self):
        return self.file_type == 'Gif'

    @property
    def is_file(self):
        return self.file_type == 'File'

    @property
    def is_contact(self):
        return self.file_type == 'Contact' or self.message_type == 'ContactMessage'

    @property
    def is_location(self):
        return self.file_type == 'Location' or self.message_type == 'Location'

    @property
    def is_poll(self):
        return self.file_type == 'Poll' or self.message_type in ('Poll', 'Poll2')

    @property
    def is_live(self):
        return self.file_type == 'Live' or self.message_type == 'Live'

    @property
    def sticker(self):
        return Data(self.sticker_raw) if isinstance(self.sticker_raw, dict) else None

    @property
    def is_sticker(self):
        return self.sticker_raw is not None

    @property
    def has_reaction(self):
        return bool(self.reactions)

    @property
    def has_metadata(self):
        return bool(self.metadata)

    @property
    def metadata_types(self):
        if not self.metadata:
            return []
        parts = self.metadata.get('meta_data_parts', []) if isinstance(self.metadata, dict) else []
        return [p.get('type', '') for p in parts]

    @property
    def event_type(self):
        return self.event_data.get('type') if isinstance(self.event_data, dict) else None

    def guid_type(self, chat_guid: str = None):
        if chat_guid is None:
            chat_guid = self.chat_guid
        if chat_guid.startswith("c0"):
            return "Channel"
        elif chat_guid.startswith("g0"):
            return "Group"
        elif chat_guid.startswith("b0"):
            return "Bot"
        elif chat_guid.startswith("s0"):
            return "Service"
        else:
            return "User"

    async def reply(self, text=None, file_inline=None, **kwargs):
        return await self.client.send_message(
            self.chat_guid, text=text,
            reply_to_message_id=self.message_id,
            file_inline=file_inline, **kwargs
        )

    async def delete(self, message_id: str = None):
        return await self.client.delete_messages(self.chat_guid, [message_id or self.message_id])

    async def forward(self, to_chat: str = None, message_id: str = None):
        return await self.client.forward_messages(
            self.chat_guid,
            [message_id or self.message_id],
            to_chat or self.chat_guid,
        )

    async def copy(self, to_chat: str = None, via_bot: str = None):
        target = to_chat or self.chat_guid
        
        if self.file_inline:
            file_path = await self.download(save_as=True)
            if not file_path:
                return

            try:
                kwargs = {}
                if self.text:
                    kwargs['text'] = self.text
                if self.thumb_inline:
                    kwargs['thumb'] = self.thumb_inline
                if self.file_width:
                    kwargs['width'] = self.file_width
                if self.file_height:
                    kwargs['height'] = self.file_height
                if self.file_duration:
                    kwargs['time'] = self.file_duration
                if via_bot:
                    kwargs['via_bot'] = via_bot

                if self.is_image:
                    return await self.client.send_image(target, file_path, **kwargs)
                elif self.is_video:
                    return await self.client.send_video(target, file_path, **kwargs)
                elif self.is_video_message:
                    return await self.client.send_video_message(target, file_path, **kwargs)
                elif self.is_voice:
                    return await self.client.send_voice(target, file_path, **kwargs)
                elif self.is_music:
                    if self.music_performer:
                        kwargs['performer'] = self.music_performer
                    return await self.client.send_music(target, file_path, **kwargs)
                elif self.is_gif:
                    return await self.client.send_gif(target, file_path, **kwargs)
                elif self.is_sticker:
                    return await self.client.send_sticker(target, file_path, **kwargs)
                else:
                    return await self.client.send_file(target, file_path, **kwargs)
            finally:
                import os
                if os.path.exists(file_path):
                    os.remove(file_path)

        elif self.text:
            reply_to = None
            if to_chat is None and self.is_reply:
                reply_to = self.reply_to_message_id
            return await self.client.send_message(
                target, text=self.text, metadata=self.metadata,
                reply_to_message_id=reply_to, via_bot=via_bot
            )

    async def pin(self):
        return await self.client.pin_message(self.chat_guid, self.message_id)

    async def unpin(self):
        return await self.client.unpin_message(self.chat_guid, self.message_id)

    async def seen(self, seen_list: dict = None):
        if seen_list is None:
            seen_list = {self.chat_guid: self.message_id}
        return await self.client.seen_chats(seen_list)

    async def add_reaction(self, reaction_id: int):
        return await self.client.add_reaction(self.chat_guid, self.message_id, reaction_id)

    async def remove_reaction(self, reaction_id: int):
        return await self.client.remove_reaction(self.chat_guid, self.message_id, reaction_id)

    async def download(self, file_inline=None, save_as=None, **kwargs):
        fi = file_inline or self.file_inline
        if isinstance(fi, dict):
            fi = Event(fi)
        return await self.client.download_file(
            fi.dc_id, fi.file_id, fi.access_hash_rec, fi.size,
            save_as=save_as, file_name=getattr(fi, 'file_name', None),
            mime=getattr(fi, 'mime', None), **kwargs
        )

    async def get_author(self):
        return await self.client.get_user_info(self.author_guid)

    async def get_chat(self):
        return await self.client.get_chat_info(self.chat_guid)

    async def ban_member(self, user_guid=None):
        return await self.client.ban_member(self.chat_guid, user_guid or self.author_guid)

    async def unban_member(self, user_guid=None):
        return await self.client.unban_member(self.chat_guid, user_guid or self.author_guid)

    async def member_is_admin(self, member_guid=None):
        return await self.client.member_is_admin(self.chat_guid, member_guid or self.author_guid)

    async def block_user(self, user_guid=None):
        return await self.client.block_user(user_guid or self.author_guid)

    async def unblock_user(self, user_guid=None):
        return await self.client.unblock_user(user_guid or self.author_guid)

    async def send_activity(self, activity: Literal["Typing", "Uploading", "Recording"] = "Typing"):
        return await self.client.send_chat_activity(self.chat_guid, activity)