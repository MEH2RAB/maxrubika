from typing import Callable, Union
import maxrubika
from .handlers import ChatUpdates, MessageUpdates, ShowActivities, ShowNotifications, RemoveNotifications

class HandlerManager:
    def add_handler(
        self: "maxrubika.Client",
        func: Callable,
        handler: Union[ChatUpdates, MessageUpdates, ShowActivities, ShowNotifications, RemoveNotifications],
    ) -> None:
        self.handlers[func] = handler

    def remove_handler(self: "maxrubika.Client", func) -> None:
        try:
            self.handlers.pop(func)
        except KeyError:
            pass