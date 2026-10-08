"""Unified envelope for all incoming bot events."""
from __future__ import annotations

import os
from ..hybrid import wrap_methods
from ..data import Data

class Events(Data):
    def __init__(self, data: dict, bot=None, **kwargs) -> None:
        super().__init__(data)
        self.bot = bot

    def _convert_value(self, value):
        if type(value) is dict:
            return Data(value)
        if type(value) is list:
            return [self._convert_value(item) for item in value]
        return value

    @staticmethod
    def _unwrap(value):
        if value is None:
            return None
        if hasattr(value, "_data"):
            return value._data
        return value

    @property
    def update_type(self):
        """Type of the update (NewMessage, EditedMessage, ...)."""
        return self.find_keys("type")

    @property
    def chat_id(self):
        """Chat ID carried by this event."""
        return self.find_keys("chat_id")

    @property
    def timestamp(self):
        """Server timestamp of the update."""
        return self.find_keys("update_time")

    @property
    def message(self):
        """New message payload (for NewMessage events)."""
        return self.find_keys("new_message")

    @property
    def edited_message(self):
        """Edited message payload (for UpdatedMessage events)."""
        return self.find_keys("updated_message")

    @property
    def deleted_message_id(self):
        """Deleted message ID (for RemovedMessage events)."""
        val = self.find_keys("removed_message_id")
        return str(val) if val is not None else None

    @property
    def callback_payload(self):
        """Full payload for InlineMessage (button click) events."""
        if self.update_type == "InlineMessage":
            return self._data
        return None

    @property
    def event_data(self):
        """Payload of EventData updates (BotJoined, BotRemoved, ...)."""
        return self.find_keys("event_data")

    @property
    def event_type(self):
        """Type inside event_data, e.g. 'BotJoined'."""
        ed = self._unwrap(self.event_data)
        return ed.get("type") if isinstance(ed, dict) else None

    @property
    def text(self):
        """Text body of the event (message, edit, or callback)."""
        return self.find_keys("text")

    @property
    def author_id(self):
        """Rubika sender ID of the person who triggered the event."""
        return self.find_keys("sender_id")

    @property
    def sender_id(self):
        """Rubika sender ID of the person who triggered the event."""
        return self.author_id

    @property
    def sender_type(self):
        """Sender type: 'User', 'Bot', etc."""
        return self.find_keys("sender_type")

    @property
    def msg_id(self):
        """Unique message identifier carried by this event."""
        if self.deleted_message_id:
            return self.deleted_message_id
        mid = self.find_keys("message_id")
        return str(mid) if mid is not None else None

    @property
    def message_id(self):
        """Unique message identifier carried by this event."""
        return self.msg_id

    @property
    def is_edited(self):
        """True if the message has been edited."""
        return bool(self.find_keys("is_edited", default=False))

    @property
    def is_deleted(self):
        """True if this event is a RemovedMessage."""
        return self.update_type == "RemovedMessage"

    @property
    def message_time(self):
        """Timestamp of the message (as string from server)."""
        return self.find_keys("time")

    @property
    def file_id(self):
        """File attachment ID if present."""
        return self.find_keys("file_id")

    @property
    def file_name(self):
        """Original file name."""
        return self.find_keys("file_name")

    @property
    def file_size(self):
        """File size in bytes."""
        return self.find_keys("size")

    @property
    def file_type(self):
        """
        Guess file type from the file extension.

        Returns one of: 'image', 'video', 'voice', 'music', 'sticker', 'file'.
        """
        if self.sticker is not None:
            return "sticker"

        name = self.file_name
        if not name:
            return None

        name_lower = name.lower()

        if name_lower.startswith("voice_"):
            return "voice"

        ext_map = {
            ".jpg": "image", ".jpeg": "image", ".jpe": "image", ".jfif": "image",
            ".png": "image", ".gif": "image", ".webp": "image", ".bmp": "image",
            ".tiff": "image", ".tif": "image", ".ico": "image", ".svg": "image",
            ".heic": "image", ".heif": "image", ".avif": "image",

            ".mp4": "video", ".m4v": "video", ".avi": "video", ".mkv": "video",
            ".mov": "video", ".wmv": "video", ".flv": "video", ".webm": "video",
            ".3gp": "video", ".3g2": "video", ".mpeg": "video", ".mpg": "video",

            ".mp3": "music", ".wav": "music", ".flac": "music", ".m4a": "music",
            ".aac": "music", ".wma": "music", ".aiff": "music", ".aif": "music",
            ".opus": "music", ".amr": "music",

            ".ogg": "voice", ".oga": "voice",
        }
        for ext, kind in ext_map.items():
            if name_lower.endswith(ext):
                return kind

        return "file"

    @property
    def sticker(self):
        """Sticker data if present."""
        return self.find_keys("sticker")

    @property
    def is_sticker(self):
        """True if this event carries a sticker."""
        return self.sticker is not None

    @property
    def sticker_id(self):
        """Sticker ID if present."""
        return self.find_keys("sticker_id")

    @property
    def poll(self):
        """Poll data if present."""
        return self.find_keys("poll")

    @property
    def is_poll(self):
        """True if this event carries a poll."""
        return self.poll is not None

    @property
    def poll_options(self):
        """Poll options list (empty if not a poll)."""
        poll = self._unwrap(self.poll)
        if isinstance(poll, dict):
            return poll.get("options", [])
        return []

    @property
    def location(self):
        """Location data if present."""
        return self.find_keys("location")

    @property
    def is_location(self):
        """True if this event carries a location."""
        return self.location is not None

    @property
    def reply_to_message_id(self):
        """ID of the message this one replies to."""
        return self.find_keys("reply_to_message_id")

    @property
    def reply_to_msg_id(self):
        """ID of the message this one replies to."""
        return self.reply_to_message_id

    @property
    def is_reply(self):
        """True if this message is a reply."""
        return self.reply_to_message_id is not None

    @property
    def forwarded_from(self):
        """Forward info (forwarded_from) if linked forward."""
        return self.find_keys("forwarded_from")

    @property
    def forwarded_no_link(self):
        """Forward info (forwarded_no_link) if sender hidden."""
        return self.find_keys("forwarded_no_link")

    @property
    def is_forwarded(self):
        """True if this message was forwarded (any type)."""
        return self.forwarded_from is not None or self.forwarded_no_link is not None

    @property
    def forward_type(self):
        """Returns 'User', 'Channel', 'Bot', or 'NoLink'."""
        ff = self._unwrap(self.forwarded_from)
        if isinstance(ff, dict):
            return ff.get("type_from")
        if self.forwarded_no_link is not None:
            return "NoLink"
        return None

    @property
    def forward_sender_id(self):
        """Original sender ID if forwarded_from is present."""
        ff = self._unwrap(self.forwarded_from)
        if isinstance(ff, dict):
            return ff.get("from_sender_id")
        return None

    @property
    def forward_chat_id(self):
        """Original chat ID if forwarded from a channel."""
        ff = self._unwrap(self.forwarded_from)
        if isinstance(ff, dict):
            return ff.get("from_chat_id")
        return None

    @property
    def forward_message_id(self):
        """Original message ID of the forwarded message."""
        ff = self._unwrap(self.forwarded_from)
        if isinstance(ff, dict):
            return ff.get("message_id")
        return None

    @property
    def forward_title(self):
        """Title if forwarded_no_link (hidden profile)."""
        fnl = self._unwrap(self.forwarded_no_link)
        if isinstance(fnl, dict):
            return fnl.get("from_title")
        return None

    @property
    def is_forwarded_from_user(self):
        """True if forwarded from a User."""
        return self.forward_type in ("User", "NoLink")

    @property
    def is_forwarded_from_channel(self):
        """True if forwarded from a Channel."""
        return self.forward_type == "Channel"

    @property
    def is_forwarded_from_bot(self):
        """True if forwarded from a Bot."""
        return self.forward_type == "Bot"

    @property
    def is_forwarded_no_link(self):
        """True if forwarded with hidden sender."""
        return self.forwarded_no_link is not None

    @property
    def aux_data(self):
        """Auxiliary data (button_id for keypad/inline clicks)."""
        return self.find_keys("aux_data")

    @property
    def button_id(self):
        """Button ID from aux_data."""
        return self.find_keys("button_id")

    @property
    def callback_data(self):
        """Full callback payload for inline button clicks."""
        return self.callback_payload

    @property
    def callback_button_id(self):
        """Button ID when update_type is InlineMessage."""
        if self.update_type == "InlineMessage":
            return self.button_id
        return None

    @property
    def metadata(self):
        """Metadata if message has formatting."""
        return self.find_keys("metadata")

    @property
    def metadata_parts(self):
        """Full metadata parts array (list of dicts)."""
        meta = self._unwrap(self.metadata)
        if not isinstance(meta, dict):
            return []
        parts = meta.get("meta_data_parts", [])
        return parts if isinstance(parts, list) else []

    @property
    def metadata_types(self):
        """List of metadata types used in this message (in message order)."""
        return list(dict.fromkeys(
            p.get("type", "")
            for p in self.metadata_parts
            if isinstance(p, dict)
        ))

    @property
    def metadata_type(self):
        """First metadata type (or None)."""
        types = self.metadata_types
        return types[0] if types else None

    @property
    def is_group(self):
        """True if the chat is a group (g0...)."""
        cid = self.chat_id
        return bool(cid) and cid.startswith("g0")

    @property
    def is_channel(self):
        """True if the chat is a channel (c0...)."""
        cid = self.chat_id
        return bool(cid) and cid.startswith("c0")

    @property
    def is_user(self):
        """True if the chat is a user chat (b0...)."""
        cid = self.chat_id
        return bool(cid) and cid.startswith("b0")

    @property
    def is_text(self):
        """True if this is a plain text message (no file/sticker/poll/location)."""
        return (
            self.text is not None
            and self.file_id is None
            and not self.is_sticker
            and not self.is_poll
            and not self.is_location
        )

    @property
    def is_image(self):
        """True if the file is an image."""
        return self.file_type == "image"

    @property
    def is_video(self):
        """True if the file is a video."""
        return self.file_type == "video"

    @property
    def is_voice(self):
        """True if the file is a voice message."""
        return self.file_type == "voice"

    @property
    def is_music(self):
        """True if the file is a music file."""
        return self.file_type == "music"

    @property
    def is_command(self):
        """True if text starts with '/'."""
        text = self.text
        return text is not None and text.startswith("/")

    @property
    def command(self):
        """Command name (without '/'), e.g. 'start' for '/start'."""
        text = self.text
        if not text or not text.startswith("/"):
            return None
        return text.split()[0][1:].split("@")[0]

    @property
    def command_args(self):
        """Arguments after the command (empty string if none)."""
        text = self.text
        if not text or not text.startswith("/"):
            return ""
        parts = text.split(maxsplit=1)
        return parts[1] if len(parts) > 1 else ""

    @property
    def pattern_match(self):
        """Regex match object stored by a regex-based filter."""
        return self._memo.get("_regex_match")

    async def ban_member(self, sender_id: str = None):
        """Ban this member or another member by sender ID."""
        target_sender_id = sender_id or self.author_id
        if not target_sender_id:
            return
        if self.chat_id and self.bot:
            return await self.bot.ban_member(
                chat_id=self.chat_id,
                sender_id=target_sender_id,
            )

    async def reply(self, text: str, **extras):
        """Send a threaded reply directly from this event."""
        if self.chat_id and self.bot:
            return await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def reply_image(self, image: str = None, **extras):
        """Send a threaded image reply."""
        if self.chat_id and self.bot:
            return await self.bot.send_image(
                chat_id=self.chat_id,
                image=image,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def reply_video(self, video: str = None, **extras):
        """Send a threaded video reply."""
        if self.chat_id and self.bot:
            return await self.bot.send_video(
                chat_id=self.chat_id,
                video=video,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def reply_gif(self, gif: str = None, **extras):
        """Send a threaded GIF reply."""
        if self.chat_id and self.bot:
            return await self.bot.send_gif(
                chat_id=self.chat_id,
                gif=gif,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def reply_music(self, music: str = None, **extras):
        """Send a threaded music reply."""
        if self.chat_id and self.bot:
            return await self.bot.send_music(
                chat_id=self.chat_id,
                music=music,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def reply_voice(self, voice: str = None, **extras):
        """Send a threaded voice reply."""
        if self.chat_id and self.bot:
            return await self.bot.send_voice(
                chat_id=self.chat_id,
                voice=voice,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def reply_file(self, file: str = None, **extras):
        """Send a threaded file reply."""
        if self.chat_id and self.bot:
            return await self.bot.send_file(
                chat_id=self.chat_id,
                file=file,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def reply_contact(self, first_name: str, phone_number, **extras):
        """Send a threaded contact reply."""
        if self.chat_id and self.bot:
            return await self.bot.send_contact(
                chat_id=self.chat_id,
                first_name=first_name,
                phone_number=phone_number,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def reply_location(self, latitude, longitude, **extras):
        """Send a threaded location reply."""
        if self.chat_id and self.bot:
            return await self.bot.send_location(
                chat_id=self.chat_id,
                latitude=latitude,
                longitude=longitude,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def reply_poll(self, question: str, options: list, **extras):
        """Send a threaded poll reply."""
        if self.chat_id and self.bot:
            return await self.bot.send_poll(
                chat_id=self.chat_id,
                question=question,
                options=options,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def reply_quiz(self, question: str, options: list, correct_option, **extras):
        """Send a threaded quiz reply."""
        if self.chat_id and self.bot:
            return await self.bot.send_quiz(
                chat_id=self.chat_id,
                question=question,
                options=options,
                correct_option=correct_option,
                reply_to_message_id=self.msg_id,
                **extras,
            )

    async def delete(self, message_id: str = None):
        """Delete this message or another by ID."""
        msg_id = message_id or self.msg_id
        if not msg_id:
            return
        if self.chat_id and self.bot:
            return await self.bot.delete_message(
                chat_id=self.chat_id,
                message_id=msg_id,
            )

    async def forward(self, to_chat_id: str = None):
        """Forward this message to another chat or same chat."""
        if not self.bot or not self.msg_id:
            return
        target_chat = to_chat_id or self.chat_id
        return await self.bot.forward_message(
            from_chat_id=self.chat_id,
            message_id=self.msg_id,
            to_chat_id=target_chat,
        )

    async def copy(self, to_chat_id: str = None):
        """Copy this message to another chat or same chat."""
        if not self.bot:
            return

        target_chat = to_chat_id or self.chat_id
        is_copy_to_other = to_chat_id is not None

        if self.file_id:
            type_map = {
                "image": "Image",
                "video": "Video",
                "voice": "Voice",
                "music": "Music",
                "file": "File",
            }
            file_type = type_map.get(self.file_type, "File")

            result = await self.bot.download_file(
                file_id=self.file_id,
                save_as=True,
            )
            if result.get("status") == "OK":
                file_path = result["file_path"]
                try:
                    kwargs = {
                        "chat_id": target_chat,
                        "file": file_path,
                        "file_type": file_type,
                        "text": self.text,
                        "metadata": self._unwrap(self.metadata)
                    }
                    if not is_copy_to_other and self.reply_to_message_id:
                        kwargs["reply_to_message_id"] = self.reply_to_message_id
                    return await self.bot.send_file(**kwargs)
                finally:
                    if os.path.exists(file_path):
                        os.remove(file_path)

        elif self.text:
            kwargs = {
                "chat_id": target_chat,
                "text": self.text,
                "metadata": self._unwrap(self.metadata)
            }
            if not is_copy_to_other and self.reply_to_message_id:
                kwargs["reply_to_message_id"] = self.reply_to_message_id
            return await self.bot.send_message(**kwargs)

    async def is_admin(self) -> bool:
        """True if the author is an admin or creator of the chat."""
        if self.chat_id and self.author_id and self.bot:
            return await self.bot.member_is_admin(self.chat_id, self.author_id)
        return False

    async def is_owner(self) -> bool:
        """True if the author is the owner (creator) of the chat."""
        if self.chat_id and self.author_id and self.bot:
            return await self.bot.member_is_owner(self.chat_id, self.author_id)
        return False

    async def is_joined(self, chat_id: str) -> bool:
        """Check if the author is a member of the given chat."""
        if self.author_id and self.bot:
            return await self.bot.member_is_joined(chat_id, self.author_id)
        return False

    async def get_chat_info(self, chat_id: str = None):
        """Get info about this chat (or another)."""
        target = chat_id or self.chat_id
        if target and self.bot:
            return await self.bot.get_chat_info(target)
        return None

    def __repr__(self) -> str:
        return f"<Events update_type={self.update_type!r} chat={self.chat_id!r}>"

wrap_methods(Events)