import inspect
import maxrubika
from ..core import handlers
from ..filters import Filter

class OnShowActivities:
    def on_show_activities(self: "maxrubika.Client", *filters: Filter):
        """Decorator for show activities (typing, uploading, recording) with optional filters."""
        def MetaHandler(func):
            async def wrapper(event):
                for f in filters:
                    if hasattr(f, 'evaluate'):
                        if not await f.evaluate(event):
                            return

                result = func(event)
                if inspect.isawaitable(result):
                    result = await result
                return result

            self.add_handler(wrapper, handlers.ShowActivities())
            return func
        return MetaHandler