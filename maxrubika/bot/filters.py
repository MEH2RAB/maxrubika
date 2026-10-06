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
from .exceptions import InvalidAccess

class EventConstraint(ABC):
    """Abstract rule that an incoming event must satisfy."""

    @abstractmethod
    async def evaluate(self, event: Any) -> bool:
        """Return True when *event* passes this constraint."""
        ...

    def __and__(self, other: "EventConstraint") -> "BothConstraint":
        return BothConstraint(self, other)

    def __or__(self, other: "EventConstraint") -> "EitherConstraint":
        return EitherConstraint(self, other)

    def __invert__(self) -> "NegateConstraint":
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

class IsEventData(EventConstraint):
    """
    Accepts EventData updates, optionally limited to given event types.

    Usage::

        IsEventData()
        IsEventData("BotJoined")
        IsEventData(["BotJoined", "BotRemoved"])
    """
    def __init__(self, event_types: Union[str, List[str], None] = None) -> None:
        if isinstance(event_types, str):
            self._types = [event_types]
        elif event_types:
            self._types = list(event_types)
        else:
            self._types = None

    async def evaluate(self, event: Any) -> bool:
        if getattr(event, 'update_type', None) != 'EventData':
            return False
        if self._types is None:
            return True
        return getattr(event, 'event_type', None) in self._types

class EventType(EventConstraint):
    """
    Matches a specific ``event_type`` inside EventData updates.

    Usage::

        EventType("BotJoined")
        EventType(["BotJoined", "BotRemoved"])
    """
    def __init__(self, event_types: Union[str, List[str]]) -> None:
        self._types: List[str] = (
            [event_types] if isinstance(event_types, str) else list(event_types)
        )

    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'event_type', None) in self._types

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
        The command name(s) without the leading slash (e.g. ``"start"``
        or ``["start", "شروع"]``). When None, any text that starts with
        a slash is accepted.
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

class IsUser(EventConstraint):
    """
    Matches events from a user chat (b0...).

    Usage::

        IsUser()
    """
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_user', False))

class IsGroup(EventConstraint):
    """
    Matches events from a group chat (g0...).

    Usage::

        IsGroup()
    """
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_group', False))

class IsChannel(EventConstraint):
    """
    Matches events from a channel (c0...).

    Usage::

        IsChannel()
    """
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_channel', False))

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
    """
    Matches any message with a file attachment (excluding stickers).

    Usage::

        IsFile()
    """
    async def evaluate(self, event: Any) -> bool:
        return (
            getattr(event, 'file_id', None) is not None
            and not getattr(event, 'is_sticker', False)
        )

class _MediaTypeConstraint(EventConstraint):
    """Base for media-specific constraints. Uses ``event.file_type``."""
    _kind: str = ''

    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'file_type', None) == self._kind

class IsImage(_MediaTypeConstraint):
    """
    Matches image files.

    Usage::

        IsImage()
    """
    _kind = 'image'

class IsVideo(_MediaTypeConstraint):
    """
    Matches video files.

    Usage::

        IsVideo()
    """
    _kind = 'video'

class IsVoice(_MediaTypeConstraint):
    """
    Matches voice messages.

    Usage::

        IsVoice()
    """
    _kind = 'voice'

class IsMusic(_MediaTypeConstraint):
    """
    Matches music files.

    Usage::

        IsMusic()
    """
    _kind = 'music'

class IsSticker(EventConstraint):
    """
    Matches sticker messages.

    Usage::

        IsSticker()
    """
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_sticker', False))

class IsPoll(EventConstraint):
    """
    Matches poll messages.

    Usage::

        IsPoll()
    """
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_poll', False))

class IsLocation(EventConstraint):
    """
    Matches location messages.

    Usage::

        IsLocation()
    """
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_location', False))

class IsReply(EventConstraint):
    """Matches messages that are a reply to another message."""
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_reply', False))

class IsText(EventConstraint):
    """Matches only plain text messages."""
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_text', False))

class IsForwarded(EventConstraint):
    """Matches any forwarded message."""
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_forwarded', False))

class ForwardedFromUser(EventConstraint):
    """Matches messages forwarded from a User (includes hidden-profile forwards)."""

    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_forwarded_from_user', False))

class ForwardedFromChannel(EventConstraint):
    """Matches messages forwarded from a Channel."""
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_forwarded_from_channel', False))

class ForwardedFromBot(EventConstraint):
    """Matches messages forwarded from a Bot."""
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_forwarded_from_bot', False))

class ForwardedNoLink(EventConstraint):
    """Matches forwarded messages where the sender has hidden their profile."""
    async def evaluate(self, event: Any) -> bool:
        return bool(getattr(event, 'is_forwarded_no_link', False))

class HasMetadata(EventConstraint):
    """Matches messages that contain metadata (Bold, Italic, Quote, etc.)."""
    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'metadata', None) is not None

class MetadataType(EventConstraint):
    """Matches messages that have specific metadata types.

    Parameters
    ----------
    types : str or list of str
        ``"Bold"``, ``"Italic"``, ``"Quote"``, ``"Monospace"``, etc.

    Usage::

        MetadataType("Bold")
        MetadataType(["Bold", "Italic"])
    """
    def __init__(self, types: Union[str, List[str]]) -> None:
        self._types: List[str] = [types] if isinstance(types, str) else list(types)

    async def evaluate(self, event: Any) -> bool:
        part_types = getattr(event, 'metadata_types', None) or []
        return any(t in self._types for t in part_types)

class IsJoined(EventConstraint):
    """
    Matches when the event author is a member of all the given chats.

    Usage::

        IsJoined("c0...")
        IsJoined(["c0A", "c0B"])
        ~IsJoined(CHAT_ID)
    """
    def __init__(self, chat_ids: Union[str, List[str]]) -> None:
        if isinstance(chat_ids, str):
            self._chat_ids: List[str] = [chat_ids]
        else:
            self._chat_ids = list(chat_ids)

    async def evaluate(self, event: Any) -> bool:
        author_id = getattr(event, "author_id", None)
        bot = getattr(event, "bot", None)
        if not author_id or bot is None:
            return False

        for chat_id in self._chat_ids:
            try:
                await bot.get_chat_member(chat_id, author_id)
            except InvalidAccess:
                return False
        return True