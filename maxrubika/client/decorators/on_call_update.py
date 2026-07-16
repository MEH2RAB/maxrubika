import maxrubika
from ..core import handlers
from ..filters import Filter

class OnCallUpdate:
    def on_call_update(self: "maxrubika.Client", *filters: Filter):
        """Decorator for call updates."""
        def MetaHandler(func):
            async def wrapper(event):
                for f in filters:
                    if hasattr(f, 'evaluate'):
                        if not await f.evaluate(event):
                            return
                return await func(event)
            self.add_handler(wrapper, handlers.CallUpdates())
            return func
        return MetaHandler