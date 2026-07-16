import maxrubika
from ..core import handlers
from ..filters import Filter

class OnDraftMessage:
    def on_draft_message(self: "maxrubika.Client", *filters: Filter):
        """Decorator for draft message updates."""
        def MetaHandler(func):
            async def wrapper(event):
                for f in filters:
                    if hasattr(f, 'evaluate'):
                        if not await f.evaluate(event):
                            return
                return await func(event)
            self.add_handler(wrapper, handlers.DraftMessageUpdate())
            return func
        return MetaHandler