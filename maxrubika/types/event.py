from typing import Literal
import maxrubika
from ..data import Data

class Event(Data):
    def __init__(self, event: dict, *args, **kwargs) -> None:
        super().__init__(event)
        self.client: "maxrubika.Client" = event.get("client")

        self._memo = {}
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
        """Return the original raw data."""
        return self._data

    @property
    def chat_guid(self):
        """Alias for object_guid."""
        return self.object_guid

    @property
    def is_me(self):
        """Check if the message was sent by the client itself."""
        return self.author_guid == self.client.guid if self.client else False

    @property
    def is_group(self):
        """Check if the chat is a group."""
        return self.object_guid.startswith('g0') if self.object_guid else False

    @property
    def is_channel(self):
        """Check if the chat is a channel."""
        return self.object_guid.startswith('c0') if self.object_guid else False

    @property
    def is_pv(self):
        """Check if the chat is a private chat (user)."""
        return self.object_guid.startswith('u0') if self.object_guid else False

    @property
    def is_bot(self):
        """Check if the chat is a bot."""
        return self.object_guid.startswith('b0') if self.object_guid else False

    @property
    def is_service(self):
        """Check if the chat is a service."""
        return self.object_guid.startswith('s0') if self.object_guid else False

    @property
    def is_text(self):
        """Check if the message is text."""
        return self.message_type == 'Text'

    @property
    def is_event(self):
        """Check if the message is an event."""
        return self.message_type == 'Event'

    @property
    def is_forward(self):
        """Check if the message is forwarded."""
        return self.forwarded_from is not None

    @property
    def is_file_inline(self):
        """Check if the message has inline file."""
        return self.message_type in ['FileInline', 'FileInlineCaption']

    @property
    def is_reply(self):
        """Check if the message is a reply."""
        return bool(self.reply_to_message_id)

    @property
    def forward_type_from(self):
        """Return the forward source type."""
        return self.forwarded_from.get('type_from', None) if isinstance(self.forwarded_from, dict) else None

    @property
    def is_forwarded_from_user(self):
        """Check if forwarded from a user."""
        return self.forward_type_from == 'User'

    @property
    def is_forwarded_from_channel(self):
        """Check if forwarded from a channel."""
        return self.forward_type_from == 'Channel'

    @property
    def is_forwarded_from_bot(self):
        """Check if forwarded from a bot."""
        return self.forward_type_from == 'Bot'

    @property
    def is_forwarded_no_link(self):
        """Check if forwarded with hidden sender."""
        return bool(self.forwarded_no_link)

    @property
    def file_inline(self):
        """Return file inline data."""
        return Data(self.file_inline_raw) if isinstance(self.file_inline_raw, dict) else None

    @property
    def message(self):
        """Return the full message data."""
        return Data(self._data.get('message', {})) if isinstance(self._data.get('message'), dict) else None

    @property
    def is_image(self):
        """Check if the message is an image."""
        return self.file_type == 'Image'

    @property
    def is_video(self):
        """Check if the message is a video."""
        return self.file_type == 'Video' and not self.is_round

    @property
    def is_video_message(self):
        """Check if the message is a round video."""
        return self.file_type == 'Video' and self.is_round

    @property
    def is_voice(self):
        """Check if the message is a voice."""
        return self.file_type == 'Voice'

    @property
    def is_music(self):
        """Check if the message is music."""
        return self.file_type == 'Music'

    @property
    def is_gif(self):
        """Check if the message is a GIF."""
        return self.file_type == 'Gif'

    @property
    def is_file(self):
        """Check if the message is a file."""
        return self.file_type == 'File'

    @property
    def is_contact(self):
        """Check if the message is a contact."""
        return self.file_type == 'Contact' or self.message_type == 'ContactMessage'

    @property
    def is_location(self):
        """Check if the message is a location."""
        return self.file_type == 'Location' or self.message_type == 'Location'

    @property
    def is_poll(self):
        """Check if the message is a poll."""
        return self.file_type == 'Poll' or self.message_type in ('Poll', 'Poll2')

    @property
    def is_live(self):
        """Check if the message is live."""
        return self.file_type == 'Live' or self.message_type == 'Live'

    @property
    def sticker(self):
        """Return sticker data."""
        return Data(self.sticker_raw) if isinstance(self.sticker_raw, dict) else None

    @property
    def is_sticker(self):
        """Check if the message is a sticker."""
        return self.sticker_raw is not None

    @property
    def has_reaction(self):
        """Check if the message has reactions."""
        return bool(self.reactions)

    @property
    def has_metadata(self):
        """Check if the message has metadata."""
        return bool(self.metadata)

    @property
    def metadata_types(self):
        """Return list of metadata types."""
        if not self.metadata:
            return []
        parts = self.metadata.get('meta_data_parts', []) if isinstance(self.metadata, dict) else []
        return [p.get('type', '') for p in parts]

    @property
    def event_type(self):
        """Return the event type."""
        return self.event_data.get('type') if isinstance(self.event_data, dict) else None

    @property
    def pattern_match(self):
        """Return regex match stored by TextMatch filter."""
        return self._memo.get('_regex_match')

    def guid_type(self, chat_guid: str = None):
        """Return the type of the chat."""
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

    async def reply(self, text: str, **extras):
        """Send a reply to this message."""
        return await self.client.send_message(
            self.chat_guid, text=text,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_image(self, image: str = None, **extras):
        """Send an image reply."""
        return await self.client.send_image(
            self.chat_guid, image=image,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_gif(self, gif: str = None, **extras):
        """Send a GIF reply."""
        return await self.client.send_gif(
            self.chat_guid, gif=gif,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_video(self, video: str = None, **extras):
        """Send a video reply."""
        return await self.client.send_video(
            self.chat_guid, video=video,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_video_message(self, video_message: str = None, **extras):
        """Send a round video reply."""
        return await self.client.send_video_message(
            self.chat_guid, video_message=video_message,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_music(self, music: str = None, **extras):
        """Send a music reply."""
        return await self.client.send_music(
            self.chat_guid, music=music,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_voice(self, voice: str = None, **extras):
        """Send a voice reply."""
        return await self.client.send_voice(
            self.chat_guid, voice=voice,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_file(self, file: str = None, **extras):
        """Send a file reply."""
        return await self.client.send_file(
            self.chat_guid, file=file,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def delete(self, message_id: str = None, **extras):
        """Delete this message."""
        return await self.client.delete_messages(
            self.chat_guid,
            [message_id or self.message_id],
            **extras
        )

    async def forward(self, to_chat: str = None, message_id: str = None, **extras):
        """Forward this message."""
        return await self.client.forward_messages(
            self.chat_guid,
            [message_id or self.message_id],
            to_chat or self.chat_guid,
            **extras
        )

    async def copy(self, to_chat: str = None, via_bot: str = None):
        """Copy this message to another chat."""
        target = to_chat or self.chat_guid

        if self.file_inline:
            file_data = await self.download()
            if not file_data:
                return

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
                kwargs['time'] = self.file_duration / 1000 if not self.is_music else self.file_duration
            if self.file_name:
                kwargs['file_name'] = self.file_name
            if self.music_performer:
                kwargs['performer'] = self.music_performer
            if via_bot:
                kwargs['via_bot'] = via_bot

            if self.is_image:
                return await self.client.send_image(target, file_data, **kwargs)
            elif self.is_video:
                return await self.client.send_video(target, file_data, **kwargs)
            elif self.is_video_message:
                return await self.client.send_video_message(target, file_data, **kwargs)
            elif self.is_voice:
                return await self.client.send_voice(target, file_data, **kwargs)
            elif self.is_music:
                return await self.client.send_music(target, file_data, **kwargs)
            elif self.is_gif:
                return await self.client.send_gif(target, file_data, **kwargs)
            else:
                return await self.client.send_file(target, file_data, **kwargs)

        elif self.is_sticker:
            sticker_data = self.sticker_raw
            if sticker_data and isinstance(sticker_data, dict):
                return await self.client.send_sticker(
                    target,
                    emoji_character=sticker_data.get('emoji_character', ''),
                    sticker_id=sticker_data.get('sticker_id', ''),
                    sticker_set_id=sticker_data.get('sticker_set_id', ''),
                    file=sticker_data.get('file', {}),
                    via_bot=via_bot
                )

        elif self.text:
            reply_to = None
            if to_chat is None and self.is_reply:
                reply_to = self.reply_to_message_id
            return await self.client.send_message(
                target, text=self.text, metadata=self.metadata,
                reply_to_message_id=reply_to, via_bot=via_bot
            )

    async def pin(self):
        """Pin this message."""
        return await self.client.pin_message(self.chat_guid, self.message_id)

    async def unpin(self):
        """Unpin this message."""
        return await self.client.unpin_message(self.chat_guid, self.message_id)

    async def seen(self, seen_list: dict = None):
        """Mark messages as seen."""
        if seen_list is None:
            seen_list = {self.chat_guid: self.message_id}
        return await self.client.seen_chats(seen_list)

    async def add_reaction(self, reaction_id: int):
        """Add reaction to this message."""
        return await self.client.add_reaction(self.chat_guid, self.message_id, reaction_id)

    async def remove_reaction(self, reaction_id: int):
        """Remove reaction from this message."""
        return await self.client.remove_reaction(self.chat_guid, self.message_id, reaction_id)

    async def download(self, file: str = None, save_as: bool = True, **extras):
        """Download the file."""
        fi = file or self.file_inline_raw

        if not isinstance(fi, dict):
            if isinstance(fi, Data):
                fi = fi.to_dict() if hasattr(fi, 'to_dict') else dict(fi)
            else:
                return None

        return await self.client.download_file(
            fi,
            save_as=save_as,
            **extras
        )

    async def get_author(self):
        """Get author information."""
        return await self.client.get_user_info(self.author_guid)

    async def get_chat(self):
        """Get chat information."""
        return await self.client.get_chat_info(self.chat_guid)

    async def ban_member(self, member=None):
        """Ban a member."""
        return await self.client.ban_member(self.chat_guid, member or self.author_guid)

    async def unban_member(self, member=None):
        """Unban a member."""
        return await self.client.unban_member(self.chat_guid, member or self.author_guid)

    async def member_is_admin(self, member=None):
        """Check if a member is admin."""
        return await self.client.member_is_admin(self.chat_guid, member or self.author_guid)

    async def block_user(self, user=None):
        """Block a user."""
        return await self.client.block_user(user or self.author_guid)

    async def unblock_user(self, user=None):
        """Unblock a user."""
        return await self.client.unblock_user(user or self.author_guid)

    async def mute_chat(self, chat=None, **extras):
        """Mute a chat."""
        return await self.client.mute_chat(chat or self.chat_guid, **extras)

    async def unmute_chat(self, chat=None, **extras):
        """Unmute a chat."""
        return await self.client.unmute_chat(chat or self.chat_guid, **extras)

    async def archive_chat(self, chat=None):
        """Archive a chat."""
        return await self.client.archive_chat(chat or self.chat_guid)

    async def unarchive_chat(self, chat=None):
        """Unarchive a chat."""
        return await self.client.unarchive_chat(chat or self.chat_guid)

    async def delete_user_chat(self, user=None):
        """Delete a user chat."""
        return await self.client.delete_user_chat(user or self.author_guid)

    async def send_activity(self, activity: Literal["Typing", "Uploading", "Recording"] = "Typing"):
        """Send chat activity."""
        return await self.client.send_chat_activity(self.chat_guid, activity)