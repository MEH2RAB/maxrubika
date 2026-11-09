from __future__ import annotations

from typing import Callable, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika
    from .handlers import ChatUpdates, MessageUpdates, ShowActivities, ShowNotifications, RemoveNotifications

class HandlerManager:
    def add_handler(
        self: "maxrubika.Messenger",
        func: Callable,
        handler: Union[ChatUpdates, MessageUpdates, ShowActivities, ShowNotifications, RemoveNotifications]
    ):
        self.handlers[func] = handler

    def remove_handler(self: "maxrubika.Messenger", func) -> None:
        try:
            self.handlers.pop(func)
        except KeyError:
            pass