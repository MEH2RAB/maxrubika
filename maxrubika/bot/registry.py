"""Core handler registry and dispatch engine."""
from __future__ import annotations

import asyncio
import inspect
import logging
from typing import Any, Callable, List, Tuple

from .filters import EventConstraint

logger = logging.getLogger(__name__)

class HandlerRegistry:
    """Central store for every registered handler and callback."""

    __slots__ = (
        '_bot',
        '_handlers',
        '_middlewares',
        '_startup_callbacks',
        '_shutdown_callbacks',
    )

    def __init__(self, bot: Any) -> None:
        self._bot = bot
        self._handlers: List[Tuple[Tuple[EventConstraint, ...], Callable]] = []
        self._middlewares: List[Callable] = []
        self._startup_callbacks: List[Callable] = []
        self._shutdown_callbacks: List[Callable] = []

    def store(self, func: Callable, *constraints: EventConstraint) -> Callable:
        """Persist a handler function with its constraints."""
        self._handlers.append((constraints, func))
        logger.debug("Stored handler %s", func.__name__)
        return func

    def store_middleware(self, func: Callable) -> Callable:
        """Add a middleware to the chain."""
        self._middlewares.append(func)
        return func

    def store_startup(self, func: Callable) -> Callable:
        """Register a startup callback."""
        self._startup_callbacks.append(func)
        return func

    def store_shutdown(self, func: Callable) -> Callable:
        """Register a shutdown callback."""
        self._shutdown_callbacks.append(func)
        return func

    async def _run_middleware_chain(self, event: Any, index: int = 0) -> None:
        if index >= len(self._middlewares):
            await self._dispatch(event)
            return

        middleware = self._middlewares[index]
        try:
            if inspect.iscoroutinefunction(middleware):
                await middleware(
                    self._bot,
                    event,
                    lambda: self._run_middleware_chain(event, index + 1),
                )
            else:
                middleware(
                    self._bot,
                    event,
                    lambda: asyncio.ensure_future(
                        self._run_middleware_chain(event, index + 1)
                    ),
                )
        except Exception:
            logger.exception("Middleware %s crashed", middleware.__name__)

    async def _invoke(self, handler: Callable, event: Any) -> None:
        """Run one handler; an exception in it never reaches the others."""
        logger.debug("Dispatching to %s", handler.__name__)
        try:
            if inspect.iscoroutinefunction(handler):
                await handler(self._bot, event)
            else:
                handler(self._bot, event)
        except Exception:
            logger.exception(
                "Handler %s raised an exception", handler.__name__
            )

    async def _dispatch(self, event: Any) -> None:
        # True: every matching handler runs (registration order does not decide
        # who is skipped). False: only the first matching handler runs.
        run_all = self._bot.run_all_handlers
        matched = False

        for constraints, handler in self._handlers:
            if await self._satisfies(event, constraints):
                matched = True
                await self._invoke(handler, event)
                if not run_all:
                    return

        if not matched:
            logger.debug("No handler matched event update_type=%s", getattr(event, 'update_type', '?'))

    @staticmethod
    async def _satisfies(
        event: Any,
        constraints: Tuple[EventConstraint, ...],
    ) -> bool:
        if not constraints:
            return True
        for c in constraints:
            try:
                if not await c.evaluate(event):
                    return False
            except Exception:
                logger.exception("Constraint %s failed", c.__class__.__name__)
                return False
        return True

    async def feed(self, event: Any) -> None:
        """Accept one incoming event and run the full pipeline."""
        await self._run_middleware_chain(event)

    async def fire_startup(self) -> None:
        for cb in self._startup_callbacks:
            try:
                if inspect.iscoroutinefunction(cb):
                    await cb(self._bot)
                else:
                    cb(self._bot)
            except Exception:
                logger.exception("Startup callback %s failed", cb.__name__)

    async def fire_shutdown(self) -> None:
        for cb in self._shutdown_callbacks:
            try:
                if inspect.iscoroutinefunction(cb):
                    await cb(self._bot)
                else:
                    cb(self._bot)
            except Exception:
                logger.exception("Shutdown callback %s failed", cb.__name__)