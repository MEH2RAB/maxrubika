from typing import TYPE_CHECKING

from ..core import handlers

if TYPE_CHECKING:
    import maxrubika

class OnRemoveNotifications:
    def on_remove_notifications(
            self: "maxrubika.Messenger",
            *args, **kwargs
    ):
        def MetaHandler(func):
            """
            Decorator to register a function as a handler for remove notifications.

            Parameters:
                func: The function to be registered as a handler.

            Returns:
                func: The original function.
            """
            self.add_handler(func, handlers.RemoveNotifications(*args, **kwargs))
            return func
        return MetaHandler