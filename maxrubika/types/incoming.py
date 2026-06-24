"""Unified envelope for all incoming bot events."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class IncomingEnvelope:
    """
    Wraps every event arriving from Rubika into a single consistent shape.

    Regardless of whether the server sent a new message, an edited message,
    a deletion notice, or an inline callback, handlers receive an instance
    of this class and can access the relevant data through the same
    properties every time.
    """
    update_type: str
    chat_id: str
    bot: Any = field(repr=False)

    message: Optional[Any] = None
    edited_message: Optional[Any] = None
    deleted_message_id: Optional[str] = None
    callback_payload: Optional[Dict[str, Any]] = None
    timestamp: Optional[int] = None
    original_data: Optional[Dict[str, Any]] = None

    _memo: Dict[str, Any] = field(default_factory=dict, repr=False)

    def _get_source(self) -> Optional[Any]:
        """Return the best source dict/object for this event."""
        if self.message is not None:
            return self.message
        if self.edited_message is not None:
            return self.edited_message
        if self.callback_payload is not None:
            return self.callback_payload
        return None

    @property
    def text(self) -> Optional[str]:
        """Text body of the event (works for message, edit, and callback)."""
        source = self._get_source()
        if source is not None:
            if isinstance(source, dict):
                return source.get('text')
            return getattr(source, 'text', None)
        return None

    @property
    def author_id(self) -> Optional[str]:
        """Rubika sender id of the person who triggered the event."""
        source = self._get_source()
        if source is not None:
            if isinstance(source, dict):
                return source.get('sender_id')
            return getattr(source, 'sender_id', None)
        return None

    @property
    def sender_type(self) -> Optional[str]:
        """Sender type: 'User', 'Bot', etc."""
        source = self._get_source()
        if source is not None:
            if isinstance(source, dict):
                return source.get('sender_type')
            return getattr(source, 'sender_type', None)
        return None

    @property
    def msg_id(self) -> Optional[str]:
        """Unique message identifier carried by this event."""
        if self.deleted_message_id:
            return self.deleted_message_id

        source = self._get_source()
        if source is not None:
            if isinstance(source, dict):
                return str(source.get('message_id', '')) or None
            return getattr(source, 'message_id', None)
        return None

    @property
    def is_edited(self) -> bool:
        """True if the message has been edited."""
        source = self.message or self.edited_message
        if source is not None:
            if isinstance(source, dict):
                return source.get('is_edited', False)
            return getattr(source, 'is_edited', False)
        return False

    @property
    def message_time(self) -> Optional[str]:
        """Timestamp of the message (as string from server)."""
        source = self.message or self.edited_message
        if source is not None:
            if isinstance(source, dict):
                return source.get('time')
            return getattr(source, 'time', None)
        return None

    @property
    def file_id(self) -> Optional[str]:
        """File attachment ID if present."""
        source = self.message or self.edited_message
        if source is not None:
            if isinstance(source, dict):
                file_data = source.get('file')
                if isinstance(file_data, dict):
                    return file_data.get('file_id')
                return source.get('file_id')
            return getattr(source, 'file_id', None)
        return None

    @property
    def file_name(self) -> Optional[str]:
        """Original file name."""
        source = self.message or self.edited_message
        if source is not None:
            if isinstance(source, dict):
                file_data = source.get('file')
                if isinstance(file_data, dict):
                    return file_data.get('file_name')
                return source.get('file_name')
            return getattr(source, 'file_name', None)
        return None

    @property
    def file_size(self) -> Optional[int]:
        """File size in bytes."""
        source = self.message or self.edited_message
        if source is not None:
            if isinstance(source, dict):
                file_data = source.get('file')
                if isinstance(file_data, dict):
                    return file_data.get('size')
                return source.get('file_size')
            return getattr(source, 'file_size', None)
        return None

    @property
    def file_type(self) -> Optional[str]:
        """
        Guess file type from file extension.

        Returns one of: 'image', 'video', 'voice', 'music', 'sticker', 'file'
        """
        name = self.file_name
        if not name:
            return None

        name_lower = name.lower()

        if name_lower.startswith('voice_') or name_lower.endswith('.ogg'):
            return 'voice'

        ext_map = {
            '.jpg': 'image', '.jpeg': 'image', '.png': 'image', '.gif': 'image', '.webp': 'image',
            '.mp4': 'video', '.avi': 'video', '.mkv': 'video', '.mov': 'video',
            '.mp3': 'music', '.wav': 'music', '.flac': 'music', '.m4a': 'music',
            '.ogg': 'voice',
            '.webm': 'sticker',
        }

        for ext, file_kind in ext_map.items():
            if name_lower.endswith(ext):
                return file_kind

        return 'file'

    @property
    def reply_to_message_id(self) -> Optional[str]:
        """ID of the message this one replies to."""
        source = self.message or self.edited_message
        if source is not None:
            if isinstance(source, dict):
                return source.get('reply_to_message_id')
            return getattr(source, 'reply_to_message_id', None)
        return None

    @property
    def forwarded_from(self) -> Optional[Dict[str, Any]]:
        """Forward info (forwarded_from) if this is a forwarded message with link."""
        source = self.message or self.edited_message
        if source is not None:
            if isinstance(source, dict):
                return source.get('forwarded_from')
            return getattr(source, 'forwarded_from', None)
        return None

    @property
    def forwarded_no_link(self) -> Optional[Dict[str, Any]]:
        """Forward info (forwarded_no_link) if sender has hidden profile."""
        source = self.message or self.edited_message
        if source is not None:
            if isinstance(source, dict):
                return source.get('forwarded_no_link')
            return getattr(source, 'forwarded_no_link', None)
        return None

    @property
    def is_forwarded(self) -> bool:
        """True if this message was forwarded (any type)."""
        return self.forwarded_from is not None or self.forwarded_no_link is not None

    @property
    def forward_type(self) -> Optional[str]:
        """Returns 'User', 'Channel', 'Bot', or 'NoLink' depending on forward type."""
        if self.forwarded_from:
            return self.forwarded_from.get('type_from')
        if self.forwarded_no_link:
            return 'NoLink'
        return None

    @property
    def forward_sender_id(self) -> Optional[str]:
        """Original sender ID if forwarded_from is present."""
        if self.forwarded_from:
            return self.forwarded_from.get('from_sender_id')
        return None

    @property
    def forward_chat_id(self) -> Optional[str]:
        """Original chat ID if forwarded from a channel."""
        if self.forwarded_from:
            return self.forwarded_from.get('from_chat_id')
        return None

    @property
    def forward_message_id(self) -> Optional[str]:
        """Original message ID of the forwarded message."""
        if self.forwarded_from:
            return self.forwarded_from.get('message_id')
        return None

    @property
    def forward_title(self) -> Optional[str]:
        """Title if forwarded_no_link (hidden profile)."""
        if self.forwarded_no_link:
            return self.forwarded_no_link.get('from_title')
        return None

    @property
    def aux_data(self) -> Optional[Dict[str, Any]]:
        """Auxiliary data (button_id for both keypad and inline clicks)."""
        source = self._get_source()
        if source is not None:
            if isinstance(source, dict):
                return source.get('aux_data')
            return getattr(source, 'aux_data', None)
        return None

    @property
    def button_id(self) -> Optional[str]:
        """Button ID from aux_data (works for both callback and keypad)."""
        aux = self.aux_data
        if aux and isinstance(aux, dict):
            return aux.get('button_id')
        return None

    @property
    def callback_data(self) -> Optional[Dict[str, Any]]:
        """Full callback payload for inline button clicks."""
        return self.callback_payload

    @property
    def callback_button_id(self) -> Optional[str]:
        """Button ID from callback (alias for button_id when update_type is InlineMessage)."""
        if self.update_type == 'InlineMessage':
            return self.button_id
        return None

    @property
    def metadata(self) -> Optional[Dict[str, Any]]:
        """Metadata if message has formatting (Bold, Italic, etc.)."""
        source = self.message or self.edited_message
        if source is not None:
            if isinstance(source, dict):
                return source.get('metadata')
            return getattr(source, 'metadata', None)
        return None

    @property
    def metadata_types(self) -> List[str]:
        """
        List of metadata types used in this message.

        Possible values: 'Bold', 'Italic', 'Quote', 'Monospace', 
        'Strikethrough', 'Underline', etc.
        """
        meta = self.metadata
        if meta:
            parts = meta.get('meta_data_parts', [])
            return list(set(p.get('type', '') for p in parts))
        return []

    @property
    def metadata_parts(self) -> List[Dict[str, Any]]:
        """Full metadata parts array."""
        meta = self.metadata
        if meta:
            return meta.get('meta_data_parts', [])
        return []

    @property
    def pattern_match(self):
        """Regex match object stored by a regex-based filter, if any."""
        return self._memo.get('_regex_match')

    async def reply(self, content: str, **extras):
        """Send a threaded reply directly from this event."""
        if self.chat_id and self.bot:
            return await self.bot.send_message(
                chat_id=self.chat_id,
                text=content,
                reply_to_message_id=self.msg_id,
                **extras
            )

    async def delete(self):
        """Delete this message."""
        if self.chat_id and self.bot and self.msg_id:
            return await self.bot.delete_message(
                chat_id=self.chat_id,
                message_id=self.msg_id
            )

    async def forward(self, to_chat_id: str = None):
        """Forward this message to another chat or repost in the same chat."""
        if not self.bot or not self.msg_id:
            return

        target_chat = to_chat_id or self.chat_id

        return await self.bot.forward_message(
            from_chat_id=self.chat_id,
            message_id=self.msg_id,
            to_chat_id=target_chat
        )

    async def copy(self, to_chat_id: str = None):
        if not self.bot:
            return

        target_chat = to_chat_id or self.chat_id
        is_copy_to_other = to_chat_id is not None

        if self.file_id:

            type_map = {
                'image': 'Image',
                'video': 'Video',
                'voice': 'Voice',
                'music': 'Music',
                'file': 'File',
            }
            file_type = type_map.get(self.file_type, 'File')

            result = await self.bot.download_file(
                file_id=self.file_id,
                save_as=True
            )
            if result["status"] == "OK":
                file_path = result["file_path"]
                try:
                    kwargs = {
                        "chat_id": target_chat,
                        "file": file_path,
                        "file_type": file_type,
                        "text": self.text,
                        "metadata": self.metadata,
                    }
                    if not is_copy_to_other and self.reply_to_message_id:
                        kwargs["reply_to_message_id"] = self.reply_to_message_id

                    response = await self.bot.send_file(**kwargs)
                    return response
                finally:
                    if os.path.exists(file_path):
                        os.remove(file_path)

        elif self.text:
            kwargs = {
                "chat_id": target_chat,
                "text": self.text,
                "metadata": self.metadata,
            }
            if not is_copy_to_other and self.reply_to_message_id:
                kwargs["reply_to_message_id"] = self.reply_to_message_id

            return await self.bot.send_message(**kwargs)

    def __repr__(self) -> str:
        return f"<IncomingEnvelope update_type={self.update_type!r} chat={self.chat_id!r}>"

    def __str__(self) -> str:
        import json
        data = {
            "update_type": self.update_type,
            "chat_id": self.chat_id,
            "msg_id": self.msg_id,
            "text": self.text,
            "author_id": self.author_id,
            "sender_type": self.sender_type,
            "is_edited": self.is_edited,
            "message_time": self.message_time,
            "timestamp": self.timestamp,
            "button_id": self.button_id,
            "aux_data": self.aux_data,
            "file_id": self.file_id,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "file_type": self.file_type,
            "reply_to_message_id": self.reply_to_message_id,
            "is_forwarded": self.is_forwarded,
            "forward_type": self.forward_type,
            "forward_sender_id": self.forward_sender_id,
            "forward_chat_id": self.forward_chat_id,
            "forward_message_id": self.forward_message_id,
            "forward_title": self.forward_title,
            "forwarded_from": self.forwarded_from,
            "forwarded_no_link": self.forwarded_no_link,
            "metadata": self.metadata,
            "metadata_types": self.metadata_types,
            "metadata_parts": self.metadata_parts,
            "original_data": self.original_data,
        }
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)