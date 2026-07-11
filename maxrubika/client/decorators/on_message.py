import maxrubika
from ..core import handlers
from ..filters import Filter

class OnMessage:
    def on_message(self: "maxrubika.Client", *filters: Filter):
        """Decorator for message updates with optional filters."""
        def MetaHandler(func):
            handler = handlers.MessageUpdates(*filters)
            self.add_handler(func, handler)
            return func
        return MetaHandler