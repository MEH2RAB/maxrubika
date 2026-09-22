import inspect
import maxrubika
from ..core import handlers
from ..filters import Filter

class OnCallSignal:
    def on_call_signal(self: "maxrubika.Client", *filters: Filter):
        """Decorator for call signal data."""
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

            self.add_handler(wrapper, handlers.CallSignalData())
            return func
        return MetaHandler