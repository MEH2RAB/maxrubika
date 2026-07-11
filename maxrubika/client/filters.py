from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Pattern, Union

class Filter(ABC):
    """Base class for all event filters."""

    @abstractmethod
    async def evaluate(self, event: Any) -> bool:
        """Return True if the event passes this filter."""
        ...

    def __and__(self, other: Filter) -> AndFilter:
        return AndFilter(self, other)

    def __or__(self, other: Filter) -> OrFilter:
        return OrFilter(self, other)

    def __invert__(self) -> NotFilter:
        return NotFilter(self)

class AndFilter(Filter):
    def __init__(self, left: Filter, right: Filter) -> None:
        self._left = left
        self._right = right

    async def evaluate(self, event: Any) -> bool:
        return await self._left.evaluate(event) and await self._right.evaluate(event)

class OrFilter(Filter):
    def __init__(self, left: Filter, right: Filter) -> None:
        self._left = left
        self._right = right

    async def evaluate(self, event: Any) -> bool:
        return await self._left.evaluate(event) or await self._right.evaluate(event)

class NotFilter(Filter):
    def __init__(self, inner: Filter) -> None:
        self._inner = inner

    async def evaluate(self, event: Any) -> bool:
        return not await self._inner.evaluate(event)

def _get_msg_text(event: Any) -> str:
    if hasattr(event, 'original_data'):
        data = event.original_data
        if isinstance(data, dict):
            msg = data.get('message', {})
            return msg.get('text', '') if isinstance(msg, dict) else ''
    return ''

def _get_msg_data(event: Any) -> dict:
    if hasattr(event, 'original_data'):
        data = event.original_data
        if isinstance(data, dict):
            return data.get('message', {})
    return {}

def _get_client(event: Any):
    return getattr(event, 'client', None) or getattr(event, '_client', None)

class IsMessage(Filter):
    """Matches new messages."""
    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'action', None) == 'New'

class IsEdited(Filter):
    """Matches edited messages."""
    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'action', None) == 'Edit'

class IsDeleted(Filter):
    """Matches deleted messages."""
    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'action', None) == 'Delete'


class ChatType(Filter):
    """
    Matches based on chat GUID prefix.
    
    Accepted values: ``"user"``, ``"bot"``, ``"group"``, ``"channel"``, ``"service"``.
    
    Usage::
        ChatType("group")
        ChatType(["group", "channel"])
    """
    _PREFIX_MAP = {'g0': 'group', 'c0': 'channel', 'u0': 'user', 'b0': 'bot', 's0': 'service'}

    def __init__(self, kinds: Union[str, List[str]]) -> None:
        self._allowed = [kinds] if isinstance(kinds, str) else list(kinds)

    async def evaluate(self, event: Any) -> bool:
        chat_id = getattr(event, 'object_guid', '')
        prefix = chat_id[:2] if chat_id else ''
        inferred = self._PREFIX_MAP.get(prefix)
        return inferred in self._allowed if inferred else False

class FromChat(Filter):
    """
    Matches events from specific chats.
    Accepts GUID, username, or link for groups/channels.
    
    Usage::
        FromChat("g0Hd4Ml...")
        FromChat("@channel_username")
        FromChat("https://rubika.ir/joing/...")
    """
    def __init__(self, chat_ids: Union[str, List[str]]) -> None:
        self._raw_ids = [chat_ids] if isinstance(chat_ids, str) else list(chat_ids)
        self._ids = []
        self._resolved = False

    async def _resolve(self, event):
        if self._resolved:
            return
        client = _get_client(event)
        if client:
            for cid in self._raw_ids:
                try:
                    resolved = await client.get_guid(cid)
                    if resolved and (resolved.startswith('g0') or resolved.startswith('c0')):
                        self._ids.append(resolved)
                except:
                    pass
        self._resolved = True

    async def evaluate(self, event: Any) -> bool:
        await self._resolve(event)
        return getattr(event, 'object_guid', '') in self._ids

class FromUser(Filter):
    """
    Matches events from specific users by author_guid or object_guid (if u0).
    
    Usage::
        FromUser("u0Hzgbk0...")
        FromUser("@Online_User")
    """
    def __init__(self, user_ids: Union[str, List[str]]) -> None:
        self._raw_ids = [user_ids] if isinstance(user_ids, str) else list(user_ids)
        self._ids = []
        self._resolved = False

    async def _resolve(self, event):
        if self._resolved:
            return
        client = _get_client(event)
        if client:
            for uid in self._raw_ids:
                try:
                    resolved = await client.get_guid(uid)
                    if resolved and resolved.startswith('u0'):
                        self._ids.append(resolved)
                except:
                    pass
        self._resolved = True

    async def evaluate(self, event: Any) -> bool:
        await self._resolve(event)
        user = getattr(event, 'author_guid', '')
        if not user:
            obj = getattr(event, 'object_guid', '')
            if obj and obj.startswith('u0'):
                user = obj
        return user in self._ids

class FromBot(Filter):
    """
    Matches events from specific bots.
    Accepts GUID, username, or link for bots.
    
    Usage::
        FromBot("b0Kiy09e...")
        FromBot("@bot_username")
    """
    def __init__(self, bot_ids: Union[str, List[str]]) -> None:
        self._raw_ids = [bot_ids] if isinstance(bot_ids, str) else list(bot_ids)
        self._ids = []
        self._resolved = False

    async def _resolve(self, event):
        if self._resolved:
            return
        client = _get_client(event)
        if client:
            for bid in self._raw_ids:
                try:
                    resolved = await client.get_guid(bid)
                    if resolved and resolved.startswith('b0'):
                        self._ids.append(resolved)
                except:
                    pass
        self._resolved = True

    async def evaluate(self, event: Any) -> bool:
        await self._resolve(event)
        author = getattr(event, 'author_guid', '')
        return author in self._ids and author.startswith('b0')

class FromActivity(Filter):
    """
    Matches typing/activity events from specific users by user_activity_guid.
    Works with on_show_activities decorator.
    
    Usage::
        FromActivity("u0Hzgbk0...")
        FromActivity("Online_User")
    """
    def __init__(self, user_ids: Union[str, List[str]]) -> None:
        self._raw_ids = [user_ids] if isinstance(user_ids, str) else list(user_ids)
        self._ids = []
        self._resolved = False

    async def _resolve(self, event):
        if self._resolved:
            return
        client = _get_client(event)
        if client:
            for uid in self._raw_ids:
                try:
                    resolved = await client.get_guid(uid)
                    if resolved and resolved.startswith('u0'):
                        self._ids.append(resolved)
                except:
                    pass
        self._resolved = True

    async def evaluate(self, event: Any) -> bool:
        await self._resolve(event)
        return getattr(event, 'user_activity_guid', '') in self._ids


class IsMe(Filter):
    """Matches messages sent by the client itself."""
    async def evaluate(self, event: Any) -> bool:
        return getattr(event, 'is_me', False)

class IsReply(Filter):
    """Matches messages that are a reply."""
    async def evaluate(self, event: Any) -> bool:
        msg = _get_msg_data(event)
        return bool(msg.get('reply_to_message_id', None)) if msg else False

class IsForwarded(Filter):
    """Matches any forwarded message."""
    async def evaluate(self, event: Any) -> bool:
        msg = _get_msg_data(event)
        return bool(msg.get('forwarded_from', None)) if msg else False

class ForwardedFromUser(Filter):
    """Matches messages forwarded from a User."""
    async def evaluate(self, event: Any) -> bool:
        fwd = _get_msg_data(event).get('forwarded_from', None)
        return fwd is not None and fwd.get('type_from', None) == 'User' if isinstance(fwd, dict) else False

class ForwardedFromChannel(Filter):
    """Matches messages forwarded from a Channel."""
    async def evaluate(self, event: Any) -> bool:
        fwd = _get_msg_data(event).get('forwarded_from', None)
        return fwd is not None and fwd.get('type_from', None) == 'Channel' if isinstance(fwd, dict) else False

class ForwardedFromBot(Filter):
    """Matches messages forwarded from a Bot."""
    async def evaluate(self, event: Any) -> bool:
        fwd = _get_msg_data(event).get('forwarded_from', None)
        return fwd is not None and fwd.get('type_from', None) == 'Bot' if isinstance(fwd, dict) else False

class ForwardedNoLink(Filter):
    """Matches forwarded messages with hidden sender profile."""
    async def evaluate(self, event: Any) -> bool:
        msg = _get_msg_data(event)
        return bool(msg.get('forwarded_no_link', None)) if msg else False

class HasReaction(Filter):
    """Matches messages that have reactions."""
    async def evaluate(self, event: Any) -> bool:
        msg = _get_msg_data(event)
        return bool(msg.get('reactions', None)) if msg else False

class IsText(Filter):
    """Matches only text messages."""
    async def evaluate(self, event: Any) -> bool:
        return bool(_get_msg_text(event)) and not getattr(event, 'file_inline', None)

class IsImage(Filter):
    """Matches image messages."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        if fi is not None and getattr(fi, 'type', None) == 'Image':
            return True
        msg = _get_msg_data(event)
        return msg.get('type') == 'Image' if msg else False

class IsVideo(Filter):
    """Matches video messages (non-round)."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        return fi is not None and getattr(fi, 'type', None) == 'Video' and not getattr(fi, 'is_round', False)

class IsVideoMessage(Filter):
    """Matches round video messages (VideoMessage)."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        return fi is not None and getattr(fi, 'type', None) == 'Video' and getattr(fi, 'is_round', False)

class IsVoice(Filter):
    """Matches voice messages."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        return fi is not None and getattr(fi, 'type', None) == 'Voice'

class IsMusic(Filter):
    """Matches music messages."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        return fi is not None and getattr(fi, 'type', None) == 'Music'

class IsGif(Filter):
    """Matches GIF messages."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        return fi is not None and getattr(fi, 'type', None) == 'Gif'

class IsSticker(Filter):
    """Matches sticker messages."""
    async def evaluate(self, event: Any) -> bool:
        if getattr(event, 'sticker', None) is not None:
            return True
        msg = _get_msg_data(event)
        return msg.get('type') == 'Sticker' if msg else False

class IsFile(Filter):
    """Matches document/file messages."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        return fi is not None and getattr(fi, 'type', None) == 'File'

class IsContact(Filter):
    """Matches contact messages."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        if fi is not None and getattr(fi, 'type', None) == 'Contact':
            return True
        msg = _get_msg_data(event)
        return msg.get('type') == 'ContactMessage' if msg else False

class IsLocation(Filter):
    """Matches location messages."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        if fi is not None and getattr(fi, 'type', None) == 'Location':
            return True
        msg = _get_msg_data(event)
        return msg.get('type') == 'Location' if msg else False

class IsPoll(Filter):
    """Matches poll messages."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        if fi is not None and getattr(fi, 'type', None) == 'Poll':
            return True
        msg = _get_msg_data(event)
        return msg.get('type') in ('Poll', 'Poll2') if msg else False

class IsLive(Filter):
    """Matches live messages."""
    async def evaluate(self, event: Any) -> bool:
        fi = getattr(event, 'file_inline', None)
        if fi is not None and getattr(fi, 'type', None) == 'Live':
            return True
        msg = _get_msg_data(event)
        return msg.get('type') == 'Live' if msg else False

class IsEvent(Filter):
    """Matches system event messages (join, leave, pin, ...)."""
    async def evaluate(self, event: Any) -> bool:
        msg = _get_msg_data(event)
        return msg.get('type') == 'Event' if msg else False

class EventType(Filter):
    """
    Matches specific system event types.
    
    Known types:
        RemoveGroupMembers, AddedGroupMembers, PinnedMessageUpdated,
        TitleUpdate, PhotoUpdate, RemovePhoto, SetAutoDelete,
        JoinedGroupByLink, LeaveGroup, JoinedGroupByRequest,
        CreateGroupVoiceChat, StopGroupVoiceChat,
        GroupCreated, ChannelCreated
    
    Usage::
        EventType("AddedGroupMembers")
        EventType("PinnedMessageUpdated")
    """
    def __init__(self, event_type: str) -> None:
        self._type = event_type

    async def evaluate(self, event: Any) -> bool:
        msg = _get_msg_data(event)
        if msg.get('type') != 'Event':
            return False
        return msg.get('event_data', {}).get('type') == self._type

class Text(Filter):
    """
    Matches when the event text contains a substring or regex pattern.

    Usage::
        Text("سلام")
        Text(r"(?i)hello")
    """
    def __init__(self, pattern: Union[str, Pattern]) -> None:
        self._regex = re.compile(pattern) if isinstance(pattern, str) else pattern

    async def evaluate(self, event: Any) -> bool:
        text = _get_msg_text(event)
        return bool(text and self._regex.search(text))

class TextMatch(Filter):
    f"""
    Like Text but stores regex match as ``event.pattern_match``.

    Usage::
        TextMatch(r"اسم من (\w+) هست")
    """
    def __init__(self, pattern: Union[str, Pattern]) -> None:
        self._regex = re.compile(pattern) if isinstance(pattern, str) else pattern

    async def evaluate(self, event: Any) -> bool:
        text = _get_msg_text(event)
        if not text:
            return False
        match = self._regex.search(text)
        if match:
            event._memo['_regex_match'] = match
            return True
        return False

class Command(Filter):
    """
    Matches bot commands like /start.

    Usage::
        Command("start")
        Command(["start", "help"])
        Command()  # any command
    """
    def __init__(self, name=None, prefixes=None):
        if isinstance(name, list):
            self._names = [n.lower().lstrip('/') for n in name]
        elif name:
            self._names = [name.lower().lstrip('/')]
        else:
            self._names = None
        self._prefixes = prefixes or ['/']

    async def evaluate(self, event: Any) -> bool:
        text = _get_msg_text(event)
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

class HasMetadata(Filter):
    """Matches messages that contain metadata (Bold, Italic, etc.)."""
    async def evaluate(self, event: Any) -> bool:
        msg = _get_msg_data(event)
        return bool(msg.get('metadata', None)) if msg else False

class MetadataType(Filter):
    """
    Matches messages with specific metadata types.

    Usage::
        MetadataType("Bold")
        MetadataType(["Bold", "Italic"])
    """
    def __init__(self, types: Union[str, List[str]]) -> None:
        self._types = [types] if isinstance(types, str) else list(types)

    async def evaluate(self, event: Any) -> bool:
        msg = _get_msg_data(event)
        if not msg:
            return False
        metadata = msg.get('metadata', None)
        if not metadata:
            return False
        parts = metadata.get('meta_data_parts', [])
        part_types = [p.get('type', '') for p in parts]
        return any(t in self._types for t in part_types)