import maxrubika
from ..core import handlers
from ..filters import Filter

class OnDeleteMessage:
    def on_delete_message(self: "maxrubika.Client", *filters: Filter):
        """Decorator for deleted messages."""
        def MetaHandler(func):
            async def wrapper(event):
                if hasattr(event, 'original_data'):
                    data = event.original_data
                else:
                    return

                if data.get('action') != 'Delete':
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