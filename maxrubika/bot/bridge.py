"""Public decorator bridge exposed on the bot instance."""
from __future__ import annotations

from .registry import HandlerRegistry
from .message import MessageDecorators
from .callback import CallbackDecorators
from .command import CommandDecorators
from .middleware import MiddlewareDecorators
from .lifecycle import LifecycleDecorators
from .event_data import EventDecorators
from .bot_status import BotStatusDecorators

class DecoratorBridge:
    """Single access point for all decorator families."""

    __slots__ = (
        '_message',
        '_callback',
        '_command',
        '_middleware',
        '_lifecycle',
        '_event',
        '_bot_status',
    )

    def __init__(self, registry: HandlerRegistry) -> None:
        self._message = MessageDecorators(registry)
        self._callback = CallbackDecorators(registry)
        self._command = CommandDecorators(registry)
        self._middleware = MiddlewareDecorators(registry)
        self._lifecycle = LifecycleDecorators(registry)
        self._event = EventDecorators(registry)
        self._bot_status = BotStatusDecorators(registry)

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

    @property
    def on_event_data(self):
        return self._event.on_event_data

    @property
    def on_bot_joined(self):
        return self._event.on_bot_joined

    @property
    def on_bot_removed(self):
        return self._event.on_bot_removed

    @property
    def on_bot_permissions_changed(self):
        return self._event.on_bot_permissions_changed

    @property
    def on_started_bot(self):
        return self._bot_status.on_started_bot

    @property
    def on_stopped_bot(self):
        return self._bot_status.on_stopped_bot

    @property
    def on_update(self):
        return self._message.on_update