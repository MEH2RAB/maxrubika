from ..hybrid import wrap_methods

from typing import Literal
import maxrubika
from ..data import Data

class Event(Data):
    def __init__(self, event: dict, *args, **kwargs) -> None:
        super().__init__(event)
        self.client: "maxrubika.Client" = event.get("client")
        self._memo = {}

    @property
    def original_data(self):
        """Return the original raw data."""
        return self._data

    @property
    def action(self):
        """Return the event action."""
        return self.find_keys("action")

    @property
    def text(self):
        """Return the message text or caption."""
        return self.find_keys(["text", "caption"])

    @property
    def message(self):
        """Return the full message data."""
        return self.find_keys("message")

    @property
    def author_title(self):
        """Return the sender display name."""
        return self.find_keys("author_title")

    @property
    def is_mine(self):
        """Check if the message was sent by the client."""
        return self.find_keys("is_mine")

    @property
    def file_inline(self):
        """Return inline file data as Data object."""
        fi = self.find_keys("file_inline")
        return Data(fi) if isinstance(fi, dict) else None

    @property
    def file_inline_raw(self):
        """Return raw inline file data as dict."""
        return self.find_keys("file_inline")

    @property
    def file_type(self):
        """Return the file type (Image, Video, Voice, ...)."""
        return self.file_inline.find_keys("type") if self.file_inline else None

    @property
    def file_name(self):
        """Return the file name."""
        return self.file_inline.find_keys("file_name") if self.file_inline else None

    @property
    def file_size(self):
        """Return the file size."""
        return self.file_inline.find_keys("size") if self.file_inline else None

    @property
    def file_dc_id(self):
        """Return the file data center ID."""
        return self.file_inline.find_keys("dc_id") if self.file_inline else None

    @property
    def file_access_hash(self):
        """Return the file access hash."""
        return self.file_inline.find_keys("access_hash_rec") if self.file_inline else None

    @property
    def file_width(self):
        """Return the file width (for images/videos)."""
        return self.file_inline.find_keys("width") if self.file_inline else None

    @property
    def file_height(self):
        """Return the file height (for images/videos)."""
        return self.file_inline.find_keys("height") if self.file_inline else None

    @property
    def file_duration(self):
        """Return the file duration (for audio/video)."""
        return self.file_inline.find_keys("time") if self.file_inline else None

    @property
    def file_mime(self):
        """Return the file MIME type."""
        return self.file_inline.find_keys("mime") if self.file_inline else None

    @property
    def thumb_inline(self):
        """Return the inline thumbnail."""
        return self.file_inline.find_keys("thumb_inline") if self.file_inline else None

    @property
    def music_performer(self):
        """Return the music performer name."""
        return self.file_inline.find_keys("music_performer") if self.file_inline else None

    @property
    def is_round(self):
        """Check if the video is a round video message."""
        return self.file_inline.find_keys("is_round") if self.file_inline else None

    @property
    def message_id(self):
        """Return the message ID."""
        return self.find_keys("message_id")

    @property
    def reply_to_message_id(self):
        """Return the ID of the message this replies to."""
        return self.find_keys("reply_to_message_id")

    @property
    def message_type(self):
        """Return the message type (Text, FileInline, ...)."""
        return self.message.find_keys("type") if self.message else None

    @property
    def author_guid(self):
        """Return the sender GUID."""
        return self.find_keys("author_object_guid")

    @property
    def type(self):
        """Return the event or author type."""
        return self.find_keys(["type", "author_type"])

    @property
    def chat_type(self):
        """Return the chat type (User, Group, Channel, ...)."""
        return self.find_keys("object_type")

    @property
    def chat_guid(self):
        """Return the chat GUID."""
        return self.find_keys("object_guid")

    @property
    def is_edited(self):
        """Check if the message was edited."""
        return self.find_keys("is_edited")

    @property
    def is_me(self):
        """Check if the message was sent by the client itself."""
        return self.author_guid == self.client.guid if self.client else False

    @property
    def is_group(self):
        """Check if the chat is a group."""
        return self.chat_guid.startswith("g0") if self.chat_guid else False

    @property
    def is_channel(self):
        """Check if the chat is a channel."""
        return self.chat_guid.startswith("c0") if self.chat_guid else False

    @property
    def is_pv(self):
        """Check if the chat is a private chat."""
        return self.chat_guid.startswith("u0") if self.chat_guid else False

    @property
    def is_bot(self):
        """Check if the chat is a bot."""
        return self.chat_guid.startswith("b0") if self.chat_guid else False

    @property
    def is_service(self):
        """Check if the chat is a service chat."""
        return self.chat_guid.startswith("s0") if self.chat_guid else False

    @property
    def is_text(self):
        """Check if the message is text."""
        return self.message_type == "Text"

    @property
    def is_event(self):
        """Check if the message is an event."""
        return self.message_type == "Event"

    @property
    def is_forward(self):
        """Check if the message is forwarded."""
        return self.find_keys("forwarded_from") is not None

    @property
    def forwarded_from(self):
        """Return the forward source info."""
        return self.find_keys("forwarded_from")

    @property
    def forwarded_no_link(self):
        """Return the forward info with hidden sender."""
        return self.find_keys("forwarded_no_link")

    @property
    def is_file_inline(self):
        """Check if the message has an inline file."""
        return self.message_type in ["FileInline", "FileInlineCaption"]

    @property
    def is_reply(self):
        """Check if the message is a reply."""
        return self.find_keys("reply_to_message_id") is not None

    @property
    def forward_type_from(self):
        """Return the forward source type."""
        return self.find_keys("type_from")

    @property
    def is_forwarded_from_user(self):
        """Check if forwarded from a user."""
        return self.forward_type_from == "User"

    @property
    def is_forwarded_from_channel(self):
        """Check if forwarded from a channel."""
        return self.forward_type_from == "Channel"

    @property
    def is_forwarded_from_bot(self):
        """Check if forwarded from a bot."""
        return self.forward_type_from == "Bot"

    @property
    def is_forwarded_no_link(self):
        """Check if forwarded with hidden sender."""
        return self.find_keys("forwarded_no_link") is not None

    @property
    def is_image(self):
        """Check if the message is an image."""
        return self.file_type == "Image"

    @property
    def is_video(self):
        """Check if the message is a video."""
        return self.file_type == "Video" and not self.is_round

    @property
    def is_video_message(self):
        """Check if the message is a video message."""
        return self.file_type == "Video" and self.is_round

    @property
    def is_voice(self):
        """Check if the message is a voice message."""
        return self.file_type == "Voice"

    @property
    def is_music(self):
        """Check if the message is music."""
        return self.file_type == "Music"

    @property
    def is_gif(self):
        """Check if the message is a GIF."""
        return self.file_type == "Gif"

    @property
    def is_file(self):
        """Check if the message is a file."""
        return self.file_type == "File"

    @property
    def is_contact(self):
        """Check if the message is a contact."""
        return self.file_type == "Contact" or self.message_type == "ContactMessage"

    @property
    def is_location(self):
        """Check if the message is a location."""
        return self.file_type == "Location" or self.message_type == "Location"

    @property
    def is_poll(self):
        """Check if the message is a poll."""
        return self.file_type == "Poll" or self.message_type in ("Poll", "Poll2")

    @property
    def is_live(self):
        """Check if the message is a live stream."""
        return self.file_type == "Live" or self.message_type == "Live"

    @property
    def sticker(self):
        """Return the sticker data."""
        s = self.find_keys("sticker")
        return Data(s) if isinstance(s, dict) else None

    @property
    def sticker_raw(self):
        """Return the raw sticker data."""
        return self.find_keys("sticker")

    @property
    def is_sticker(self):
        """Check if the message is a sticker."""
        return self.sticker_raw is not None

    @property
    def has_reaction(self):
        """Check if the message has reactions."""
        return self.find_keys("reaction") is not None

    @property
    def reactions(self):
        """Return the reactions data."""
        return self.find_keys("reaction")

    @property
    def has_metadata(self):
        """Check if the message has metadata."""
        return self.find_keys("metadata")

    @property
    def metadata(self):
        """Return the message metadata."""
        return self.find_keys("metadata")

    @property
    def metadata_types(self):
        """Return the list of metadata types."""
        if not self.has_metadata:
            return []
        parts = self.find_keys("meta_data_parts", default=[])
        return [p.get("type", "") for p in parts]

    @property
    def event_data(self):
        """Return the event data."""
        return self.find_keys("event_data")

    @property
    def event_type(self):
        """Return the event type."""
        return self.event_data.get("type") if self.event_data else None

    @property
    def timestamp(self):
        """Return the event timestamp."""
        return self.find_keys("timestamp")

    @property
    def user_activity_guid(self):
        """Return the user activity GUID."""
        return self.find_keys("user_activity_guid")

    @property
    def updated_parameters(self):
        """Return the list of updated parameters."""
        return self.find_keys("updated_parameters")

    @property
    def pattern_match(self):
        """Return regex match stored by TextMatch filter."""
        return self._memo.get('_regex_match')

    def guid_type(self, chat_guid: str = None):
        """Return the type of a chat GUID (User, Group, Channel, Bot, Service)."""
        if chat_guid is None:
            chat_guid = self.chat_guid
        if not chat_guid:
            return None
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

    async def reply(self, text=None, **kwargs):
        """Send a reply to this message."""
        return await self.client.send_message(
            self.chat_guid,
            text=text,
            reply_to_message_id=self.message_id,
            **kwargs
        )

    async def reply_image(self, image: str = None, **extras):
        """Send a threaded image reply."""
        return await self.client.send_image(
            self.chat_guid,
            image=image,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_video(self, video: str = None, **extras):
        """Send a threaded video reply."""
        return await self.client.send_video(
            self.chat_guid,
            video=video,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_video_message(self, video_message: str = None, **extras):
        """Send a threaded round video reply."""
        return await self.client.send_video_message(
            self.chat_guid,
            video_message=video_message,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_gif(self, gif: str = None, **extras):
        """Send a threaded GIF reply."""
        return await self.client.send_gif(
            self.chat_guid,
            gif=gif,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_music(self, music: str = None, **extras):
        """Send a threaded music reply."""
        return await self.client.send_music(
            self.chat_guid,
            music=music,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_voice(self, voice: str = None, **extras):
        """Send a threaded voice reply."""
        return await self.client.send_voice(
            self.chat_guid,
            voice=voice,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def reply_file(self, file: str = None, **extras):
        """Send a threaded file reply."""
        return await self.client.send_file(
            self.chat_guid,
            file=file,
            reply_to_message_id=self.message_id,
            **extras
        )

    async def edit(self, text: str, message_id: str = None, **extras):
        """Edit this message."""
        return await self.client.edit_message(
            chat=self.chat_guid,
            text=text,
            message_id=message_id or self.message_id,
            **extras
        )

    async def delete(self, message_id: str = None):
        """Delete this message."""
        return await self.client.delete_messages(
            self.chat_guid, [message_id or self.message_id]
        )

    async def forward(
        self,
        to_chat: str = None,
        message_id: str = None,
        hide_author: bool = None,
        **kwargs
    ):
        """Forward this message to another chat."""
        return await self.client.forward_messages(
            from_chat=self.chat_guid,
            message_ids=[message_id or self.message_id],
            to_chat=to_chat or self.chat_guid,
            hide_author=hide_author,
            **kwargs
        )

    async def copy(self, to_chat: str = None, via_bot: str = None):
        """Copy this message."""
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
        """Add a reaction to this message."""
        return await self.client.add_reaction(
            self.chat_guid, self.message_id, reaction_id
        )

    async def remove_reaction(self, reaction_id: int):
        """Remove a reaction from this message."""
        return await self.client.remove_reaction(
            self.chat_guid, self.message_id, reaction_id
        )

    async def download(self, file: str = None, save_as: bool = True, **extras):
        """Download the file attached to this message."""
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
        """Get the author information."""
        return await self.client.get_user_info(self.author_guid)

    async def get_chat(self):
        """Get the chat information."""
        return await self.client.get_chat_info(self.chat_guid)

    async def ban_member(self, user=None):
        """Ban a member from the chat."""
        return await self.client.ban_member(
            self.chat_guid, user or self.author_guid
        )

    async def unban_member(self, user=None):
        """Unban a member from the chat."""
        return await self.client.unban_member(
            self.chat_guid, user or self.author_guid
        )

    async def member_is_admin(self, member=None):
        """Check if a member is an admin."""
        return await self.client.member_is_admin(
            self.chat_guid, member or self.author_guid
        )

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

    async def send_activity(
        self, activity: Literal["Typing", "Uploading", "Recording"] = "Typing"
    ):
        """Send chat activity (Typing, Uploading, Recording)."""
        return await self.client.send_chat_activity(self.chat_guid, activity)

wrap_methods(Event)