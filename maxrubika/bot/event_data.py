"""Decorators for EventData updates: bot joined, removed, permissions changed, ..."""
from __future__ import annotations

from typing import Callable

from .filters import EventConstraint, IsEventData
from .registry import HandlerRegistry

class EventDecorators:
    """Decorators that fire on EventData updates."""
    __slots__ = ('_registry',)

    def __init__(self, registry: HandlerRegistry) -> None:
        self._registry = registry

    def on_event_data(self, *constraints: EventConstraint) -> Callable:
        """Handle every EventData update, whatever its event type."""
        merged = (IsEventData(),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco

    def on_bot_joined(self, *constraints: EventConstraint) -> Callable:
        """Handle the bot being added to a chat."""
        merged = (IsEventData('BotJoined'),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco

    def on_bot_removed(self, *constraints: EventConstraint) -> Callable:
        """Handle the bot being removed from a chat."""
        merged = (IsEventData('BotRemoved'),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco

    def on_bot_permissions_changed(self, *constraints: EventConstraint) -> Callable:
        """Handle a change in the bot's permissions in a chat."""
        merged = (IsEventData('BotPermissionsChanged'),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco