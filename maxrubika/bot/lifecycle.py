"""Decorators for bot startup and shutdown hooks."""

from __future__ import annotations

from typing import Callable

from .registry import HandlerRegistry

class LifecycleDecorators:
    """Decorators that fire when the bot starts or stops."""

    __slots__ = ('_registry',)

    def __init__(self, registry: HandlerRegistry) -> None:
        self._registry = registry

    def on_start(self) -> Callable:
        """Register a callback that runs once when the bot starts."""
        def deco(func: Callable) -> Callable:
            return self._registry.store_startup(func)
        return deco

    def on_shutdown(self) -> Callable:
        """Register a callback that runs when the bot shuts down."""
        def deco(func: Callable) -> Callable:
            return self._registry.store_shutdown(func)
        return deco