"""
Constraint system that decides which events should trigger a handler.

Every constraint implements a single ``evaluate`` method that inspects an
incoming event and returns True or False.  Constraints can be combined
with ``&``, ``|`` and ``~`` to build expressive matching rules without
writing nested if-blocks in every handler.
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Pattern, Union

class EventConstraint(ABC):
    """Abstract rule that an incoming event must satisfy."""

    @abstractmethod
    async def evaluate(self, event: Any) -> bool:
        """Return True when *event* passes this constraint."""
        ...

    def __and__(self, other: EventConstraint) -> BothConstraint:
        return BothConstraint(self, other)

    def __or__(self, other: EventConstraint) -> EitherConstraint:
        return EitherConstraint(self, other)

    def __invert__(self) -> NegateConstraint:
        return NegateConstraint(self)

class BothConstraint(EventConstraint):
    """Requires two constraints to pass (AND)."""

    def __init__(self, left: EventConstraint, right: EventConstraint) -> None:
        self._left = left
        self._right = right

    async def evaluate(self, event: Any) -> bool:
        return await self._left.evaluate(event) and await self._right.evaluate(event)

class EitherConstraint(EventConstraint):
    """Requires at least one constraint to pass (OR)."""

    def __init__(self, left: EventConstraint, right: EventConstraint) -> None:
        self._left = left
        self._right = right

    async def evaluate(self, event: Any) -> bool:
        return await self._left.evaluate(event) or await self._right.evaluate(event)

class NegateConstraint(EventConstraint):
    """Inverts the result of a constraint (NOT)."""

    def __init__(self, inner: EventConstraint) -> None:
        self._inner = inner

    async def evaluate(self, event: Any) -> bool:
        return not await self._inner.evaluate(event)

class IsMessage(EventConstraint):
    """Accepts only events that contain a brand-new message."""

    async def evaluate(self, event: Any) -> bool:
        return (
            getattr(event, 'update_type', None) == 'NewMessage'
            and getattr(event, 'message', None) is not None
        )

class IsEdited(EventConstraint):
    """Accepts only events that are message edits."""

    async def evaluate(self, event: Any) -> bool:
        return (
            getattr(event, 'update_type', None) == 'UpdatedMessage'
            and getattr(event, 'edited_message', None) is not None
        )

class IsDeleted(EventConstraint):
    """Accepts deleted notices."""

    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'update_type', None) == 'RemovedMessage'

class IsCallback(EventConstraint):
    """Accepts inline-keyboard callback events."""

    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'update_type', None) == 'InlineMessage'

class IsStartedBot(EventConstraint):
    """Accepts when a user starts the bot."""

    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'update_type', None) == 'StartedBot'

class IsStoppedBot(EventConstraint):
    """Accepts when a user stops the bot."""

    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'update_type', None) == 'StoppedBot'

class Text(EventConstraint):
    """
    Matches when the event text contains a substring or regex pattern.

    Usage::
    
        Text("سلام")
        Text(r"(?i)hello")
    """
    def __init__(self, pattern: Union[str, Pattern]) -> None:
        if isinstance(pattern, str):
            self._regex = re.compile(pattern)
        else:
            self._regex = pattern

    async def evaluate(self, event: Any) -> bool:
        text = getattr(event, 'text', None)
        if text is None:
            return False
        return bool(self._regex.search(text))

class TextMatch(EventConstraint):
    r"""
    Like *Text* but also stores the regex match on the event
    so the handler can access named groups via ``event.pattern_match``.

    Usage::

        TextMatch(r"اسم من (\w+) هست")
    """
    def __init__(self, pattern: Union[str, Pattern]) -> None:
        if isinstance(pattern, str):
            self._regex = re.compile(pattern)
        else:
            self._regex = pattern

    async def evaluate(self, event: Any) -> bool:
        text = getattr(event, 'text', None)
        if text is None:
            return False
        match = self._regex.search(text)
        if match:
            event._memo['_regex_match'] = match
            return True
        return False

class Command(EventConstraint):
    """
    Matches when the event text begins with a bot command like ``/start``.

    Parameters
    ----------
    name : str, list of str, or None
        The command name(s) without the leading slash (e.g. ``"start"`` or ``["start", "شروع"]``).
        When None, any text that starts with a slash is accepted.
    prefixes : list of str
        Characters that count as a command prefix (default ``["/"]``).

    Usage::

        Command("start")
        Command(["start", "شروع"])
        Command()
    """
    def __init__(
        self,
        name: Union[str, List[str], None] = None,
        prefixes: Optional[List[str]] = None,
    ) -> None:
        if isinstance(name, list):
            self._names = [n.lower().lstrip('/') for n in name]
        elif name:
            self._names = [name.lower().lstrip('/')]
        else:
            self._names = None
        self._prefixes = prefixes or ['/']

    async def evaluate(self, event: Any) -> bool:
        text = getattr(event, 'text', None)
        if not text:
            return False

        if not any(text.startswith(p) for p in self._prefixes):
            return False

        if self._names is None:
            return True

        first_token = text.split()[0]
        for prefix in self._prefixes:
            if first_token.startswith(prefix):
                first_token = first_token[len(prefix):]
                break

        first_token = first_token.split('@')[0]
        return first_token.lower() in self._names

class ChatType(EventConstraint):
    """
    Matches based on the chat type encoded in the chat_id prefix.

    Accepted values: ``"user"`` (b0...), ``"group"`` (g0...),
    ``"channel"`` (c0...).

    Usage::

        ChatType("user")
        ChatType(["group", "channel"])
    """
    _PREFIX_MAP = {'g0': 'group', 'c0': 'channel', 'b0': 'user'}

    def __init__(self, kinds: Union[str, List[str]]) -> None:
        self._allowed: List[str] = [kinds] if isinstance(kinds, str) else list(kinds)

    async def evaluate(self, event: Any) -> bool:
        chat_id = getattr(event, 'chat_id', '')
        prefix = chat_id[:2] if chat_id else ''
        inferred = self._PREFIX_MAP.get(prefix)
        return inferred in self._allowed if inferred else False

class FromChat(EventConstraint):
    """Matches when the event comes from one of the specified chat ids."""

    def __init__(self, chat_ids: Union[str, List[str]]) -> None:
        self._ids: List[str] = [chat_ids] if isinstance(chat_ids, str) else list(chat_ids)

    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'chat_id', '') in self._ids

class FromUser(EventConstraint):
    """Matches when the event author is one of the given user ids."""

    def __init__(self, user_ids: Union[str, List[str]]) -> None:
        self._ids: List[str] = [user_ids] if isinstance(user_ids, str) else list(user_ids)

    async def evaluate(self, event: Any) -> bool:
        author = getattr(event, 'author_id', None)
        return author in self._ids if author else False

class IsFile(EventConstraint):
    """Matches any message with a file attachment (generic).

    Usage::
        IsFile()
    """
    async def evaluate(self, event: Any) -> bool:
        msg = getattr(event, 'message', None) or getattr(event, 'edited_message', None)
        if msg is None:
            return False

        if isinstance(msg, dict):
            file_data = msg.get('file')
            if isinstance(file_data, dict) and file_data.get('file_id'):
                return True
            if msg.get('file_id'):
                return True
            return False

        return bool(getattr(msg, 'file_id', None))

class _MediaTypeConstraint(EventConstraint):
    """Base for media-specific constraints. Checks file extension."""

    _extensions: List[str] = []
    _voice_prefix: bool = False

    async def evaluate(self, event: Any) -> bool:
        name = getattr(event, 'file_name', None)
        if not name:
            return False

        name_lower = name.lower()

        if self._voice_prefix and name_lower.startswith('voice_'):
            return True

        return any(name_lower.endswith(ext) for ext in self._extensions)

class IsImage(_MediaTypeConstraint):
    """
    Matches image files (.jpg, .jpeg, .png, .gif, .webp).

    Usage::
        IsImage()
    """
    _extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

class IsVideo(_MediaTypeConstraint):
    """
    Matches video files (.mp4, .avi, .mkv, .mov).

    Usage::
        IsVideo()
    """
    _extensions = ['.mp4', '.avi', '.mkv', '.mov']

class IsVoice(_MediaTypeConstraint):
    """
    Matches voice messages (.ogg or starts with voice_).

    Usage::
        IsVoice()
    """
    _extensions = ['.ogg']
    _voice_prefix = True

class IsMusic(_MediaTypeConstraint):
    """
    Matches music files (.mp3, .wav, .flac, .m4a).

    Usage::
        IsMusic()
    """
    _extensions = ['.mp3', '.wav', '.flac', '.m4a']

class IsSticker(_MediaTypeConstraint):
    """
    Matches sticker files (.webm).

    Usage::
        IsSticker()
    """
    _extensions = ['.webm']

class IsReply(EventConstraint):
    """Matches messages that are a reply to another message."""

    async def evaluate(self, event: Any) -> bool:
        msg = getattr(event, 'message', None) or getattr(event, 'edited_message', None)
        if msg is None:
            return False

        if isinstance(msg, dict):
            return msg.get('reply_to_message_id') is not None

        return bool(getattr(msg, 'reply_to_message_id', None))

class IsText(EventConstraint):
    """Matches only text messages (no file, no sticker, no voice)."""

    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'text', None)) and not bool(getattr(event, 'file_id', None))

class IsForwarded(EventConstraint):
    """Matches any forwarded message (forwarded_from OR forwarded_no_link)."""

    async def evaluate(self, event: Any) -> bool:
        msg = getattr(event, 'message', None) or getattr(event, 'edited_message', None)
        if msg is None:
            return False

        if isinstance(msg, dict):
            return msg.get('forwarded_from') is not None or msg.get('forwarded_no_link') is not None

        return bool(getattr(msg, 'forwarded_from', None) or getattr(msg, 'forwarded_no_link', None))

class ForwardedFromUser(EventConstraint):
    """Matches messages forwarded from a User."""

    async def evaluate(self, event: Any) -> bool:
        msg = getattr(event, 'message', None) or getattr(event, 'edited_message', None)
        if msg is None:
            return False

        if isinstance(msg, dict):
            fwd = msg.get('forwarded_from')
            if fwd:
                return fwd.get('type_from') == 'User'
            return msg.get('forwarded_no_link') is not None
        return False

class ForwardedFromChannel(EventConstraint):
    """Matches messages forwarded from a Channel."""

    async def evaluate(self, event: Any) -> bool:
        msg = getattr(event, 'message', None) or getattr(event, 'edited_message', None)
        if msg is None:
            return False

        if isinstance(msg, dict):
            fwd = msg.get('forwarded_from')
            if fwd:
                return fwd.get('type_from') == 'Channel'
        return False

class ForwardedFromBot(EventConstraint):
    """Matches messages forwarded from a Bot."""

    async def evaluate(self, event: Any) -> bool:
        msg = getattr(event, 'message', None) or getattr(event, 'edited_message', None)
        if msg is None:
            return False

        if isinstance(msg, dict):
            fwd = msg.get('forwarded_from')
            if fwd:
                return fwd.get('type_from') == 'Bot'
        return False

class ForwardedNoLink(EventConstraint):
    """Matches forwarded messages where the sender has hidden their profile."""

    async def evaluate(self, event: Any) -> bool:
        msg = getattr(event, 'message', None) or getattr(event, 'edited_message', None)
        if msg is None:
            return False

        if isinstance(msg, dict):
            return msg.get('forwarded_no_link') is not None

        return bool(getattr(msg, 'forwarded_no_link', None))

class HasMetadata(EventConstraint):
    """Matches messages that contain metadata (Bold, Italic, Quote, etc.)."""

    async def evaluate(self, event: Any) -> bool:
        meta = getattr(event, 'metadata', None)
        if meta is not None:
            return True

        msg = getattr(event, 'message', None) or getattr(event, 'edited_message', None)
        if msg is not None and isinstance(msg, dict):
            if msg.get('metadata'):
                return True

        return False

class MetadataType(EventConstraint):
    """Matches messages that have specific metadata types.

    Parameters
    ----------
    types : str or list of str
        ``"Bold"``, ``"Italic"``, ``"Quote"``, ``"Monospace"``, etc.
    """
    def __init__(self, types: Union[str, List[str]]) -> None:
        self._types: List[str] = [types] if isinstance(types, str) else list(types)

    async def evaluate(self, event: Any) -> bool:
        part_types = getattr(event, 'metadata_types', None)
        if part_types is not None:
            return any(t in self._types for t in part_types)

        msg = getattr(event, 'message', None) or getattr(event, 'edited_message', None)
        if msg is not None and isinstance(msg, dict):
            metadata = msg.get('metadata')
            if metadata:
                parts = metadata.get('meta_data_parts', [])
                part_types = [p.get('type', '') for p in parts]
                return any(t in self._types for t in part_types)

        return False