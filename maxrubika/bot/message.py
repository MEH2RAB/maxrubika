"""Decorators for message-related events: new, edited, deleted."""
from __future__ import annotations

from typing import Callable

from .filters import (
    EventConstraint,
    IsMessage, IsEdited, IsDeleted, IsCallback,
)
from .registry import HandlerRegistry

class MessageDecorators:
    """Decorators that fire on message-level events."""
    __slots__ = ('_registry',)

    def __init__(self, registry: HandlerRegistry) -> None:
        self._registry = registry

    def on_update(self, *constraints: EventConstraint) -> Callable:
        """
        Handle *any* update type the server may send
        (NewMessage, UpdatedMessage, RemovedMessage, InlineMessage,
        StartedBot, StoppedBot, EventData, ...).

        Prefer the specific decorators (``on_message``, ``on_new_message``,
        ``on_edit_message``, ...) whenever possible.

        Usage::

            @bot.on_update()
            async def handler(bot, event):
                print(event.update_type)

            @bot.on_update(IsGroup())
            async def group_handler(bot, event):
                print(event.update_type)
        """
        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *constraints)
        return deco

    def on_new_message(self, *constraints: EventConstraint) -> Callable:
        """Handle brand-new messages."""
        merged = (IsMessage(),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco

    def on_edit_message(self, *constraints: EventConstraint) -> Callable:
        """Handle edited messages."""
        merged = (IsEdited(),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco

    def on_delete_message(self, *constraints: EventConstraint) -> Callable:
        """Handle deleted messages."""
        merged = (IsDeleted(),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco

    def on_message(self, *constraints: EventConstraint) -> Callable:
        """
        Handle any message-related event:
        NewMessage, UpdatedMessage, RemovedMessage, or InlineMessage.
        """
        merged = (
            IsMessage() | IsEdited() | IsDeleted() | IsCallback(),
        ) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco