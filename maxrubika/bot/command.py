"""Decorator shortcut for bot commands like /start."""

from __future__ import annotations

from typing import Callable, List, Optional, Union

from .filters import EventConstraint, IsMessage, Command
from .registry import HandlerRegistry

class CommandDecorators:
    """Decorator that combines message + command filtering."""

    __slots__ = ('_registry',)

    def __init__(self, registry: HandlerRegistry) -> None:
        self._registry = registry

    def on_command(
        self,
        name: Union[str, List[str], None] = None,
        *constraints: EventConstraint,
        prefixes: Optional[List[str]] = None,
    ) -> Callable:
        """
        Handle a specific bot command (or list of commands).

        Usage:

            @bot.on_command("start")
            @bot.on_command(["start", "شروع"])
            @bot.on_command()
        """
        merged = (
            IsMessage(),
            Command(name, prefixes=prefixes),
        ) + constraints

        def deco(func: Callable) -> Callable:
            return self._registry.store(func, *merged)
        return deco