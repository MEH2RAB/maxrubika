"""Decorator for middleware functions."""

from __future__ import annotations

from typing import Callable

from .registry import HandlerRegistry

class MiddlewareDecorators:
    """Decorator that registers middleware into the processing chain."""

    __slots__ = ('_registry',)

    def __init__(self, registry: HandlerRegistry) -> None:
        self._registry = registry

    def middleware(self) -> Callable:
        """Register an async middleware.

        Middleware receives ``(bot, event, call_next)`` and **must**
        call ``await call_next()`` to continue processing.
        """
        def deco(func: Callable) -> Callable:
            return self._registry.store_middleware(func)
        return deco