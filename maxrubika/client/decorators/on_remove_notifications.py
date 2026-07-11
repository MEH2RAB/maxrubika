import maxrubika
from ..core import handlers

class OnRemoveNotifications:
    def on_remove_notifications(
            self: "maxrubika.Client",
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