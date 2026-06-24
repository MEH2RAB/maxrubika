"""Public decorator bridge exposed on the bot instance."""

from __future__ import annotations

from .registry import HandlerRegistry
from .message import MessageDecorators
from .callback import CallbackDecorators
from .command import CommandDecorators
from .middleware import MiddlewareDecorators
from .lifecycle import LifecycleDecorators

class DecoratorBridge:
    """Single access point for all decorator families."""

    __slots__ = (
        '_message',
        '_callback',
        '_command',
        '_middleware',
        '_lifecycle',
    )

    def __init__(self, registry: HandlerRegistry) -> None:
        self._message = MessageDecorators(registry)
        self._callback = CallbackDecorators(registry)
        self._command = CommandDecorators(registry)
        self._middleware = MiddlewareDecorators(registry)
        self._lifecycle = LifecycleDecorators(registry)

    @property
    def on_new_message(self):
        return self._message.on_new_message

    @property
    def on_edit_message(self):
        return self._message.on_edit_message

    @property
    def on_delete_message(self):
        return self._message.on_delete_message

    @property
    def on_message(self):
        return self._message.on_message

    @property
    def on_callback(self):
        return self._callback.on_callback

    @property
    def on_command(self):
        return self._command.on_command

    @property
    def middleware(self):
        return self._middleware.middleware

    @property
    def on_start(self):
        return self._lifecycle.on_start

    @property
    def on_shutdown(self):
        return self._lifecycle.on_shutdown