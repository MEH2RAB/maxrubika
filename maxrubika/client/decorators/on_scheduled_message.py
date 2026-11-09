import inspect
from typing import TYPE_CHECKING

from ..core import handlers
from ..filters import Filter

if TYPE_CHECKING:
    import maxrubika

class OnScheduledMessage:
    def on_scheduled_message(self: "maxrubika.Messenger", *filters: Filter):
        """Decorator for scheduled message updates."""
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

            self.add_handler(wrapper, handlers.ScheduleMessageUpdates())
            return func
        return MetaHandler