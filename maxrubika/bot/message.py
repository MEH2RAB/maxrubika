"""Decorators for message-related events: new, edited, deleted."""

from __future__ import annotations

from typing import Callable

from .filters import EventConstraint, IsMessage, IsEditedMessage, IsDeleted
from .registry import HandlerRegistry

class MessageDecorators:
    """Decorators that fire on message-level events."""

    __slots__ = ('_registry',)

    def __init__(self, registry: HandlerRegistry) -> None:
        self._registry = registry

    def on_new_message(self, *constraints: EventConstraint) -> Callable:
        """Handle brand-new messages."""
        merged = (IsMessage(),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco

    def on_edit_message(self, *constraints: EventConstraint) -> Callable:
        """Handle edited messages."""
        merged = (IsEditedMessage(),) + constraints

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
        """Handle *every* event update_type (use sparingly)."""
        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *constraints)
        return deco