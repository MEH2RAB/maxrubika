"""Decorator for inline-keyboard callbacks."""

from __future__ import annotations

from typing import Callable

from .filters import EventConstraint, IsCallback
from .registry import HandlerRegistry

class CallbackDecorators:
    """Decorators that fire on inline-keyboard interactions."""

    __slots__ = ('_registry',)

    def __init__(self, registry: HandlerRegistry) -> None:
        self._registry = registry

    def on_callback(self, *constraints: EventConstraint) -> Callable:
        """Handle inline-keyboard button presses."""
        merged = (IsCallback(),) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco