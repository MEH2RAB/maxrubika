import maxrubika
from ..core import handlers
from ..filters import Filter

class OnChatUpdates:
    def on_chat_updates(self: "maxrubika.Client", *filters: Filter):
        """Decorator for chat updates with optional filters."""
        def MetaHandler(func):
            async def wrapper(event):
                for f in filters:
                    if hasattr(f, 'evaluate'):
                        if not await f.evaluate(event):
                            return
                return await func(event)

            self.add_handler(wrapper, handlers.ChatUpdates())
            return func
        return MetaHandler