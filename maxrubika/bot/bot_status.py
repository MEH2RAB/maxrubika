"""Decorators for a user starting or stopping the bot."""
from __future__ import annotations

from typing import Callable

from .filters import EventConstraint, IsStartedBot, IsStoppedBot
from .registry import HandlerRegistry

class BotStatusDecorators:
    """Decorators that fire when a user starts or stops the bot."""

    __slots__ = ('_registry',)

    def __init__(self, registry: HandlerRegistry) -> None:
        self._registry = registry

    def on_started_bot(self, *constraints: EventConstraint) -> Callable:
        """Handle a user starting the bot."""
        merged = (IsStartedBot(),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco

    def on_stopped_bot(self, *constraints: EventConstraint) -> Callable:
        """Handle a user stopping the bot."""
        merged = (IsStoppedBot(),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco