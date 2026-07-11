import maxrubika
from ..core import handlers
from ..filters import Filter

class OnShowNotifications:
    def on_show_notifications(self: "maxrubika.Client", *filters: Filter):
        """Decorator for show notifications with optional filters."""
        def MetaHandler(func):
            async def wrapper(event):
                for f in filters:
                    if hasattr(f, 'evaluate'):
                        if not await f.evaluate(event):
                            return
                return await func(event)

            self.add_handler(wrapper, handlers.ShowNotifications())
            return func
        return MetaHandler