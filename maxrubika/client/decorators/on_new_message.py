import maxrubika
from ..core import handlers
from ..filters import Filter

class OnNewMessage:
    def on_new_message(self: "maxrubika.Client", *filters: Filter):
        """Decorator for new messages with optional filters."""
        def MetaHandler(func):
            async def wrapper(event):
                if hasattr(event, 'original_data'):
                    data = event.original_data
                else:
                    return

                if data.get('action') != 'New':
                    return

                for f in filters:
                    if hasattr(f, 'evaluate'):
                        if not await f.evaluate(event):
                            return

                return await func(event)

            handler = handlers.MessageUpdates()
            self.add_handler(wrapper, handler)
            return func
        return MetaHandler