import inspect
import maxrubika
from ..core import handlers
from ..filters import Filter

class OnUnconfirmedSession:
    def on_unconfirmed_session(self: "maxrubika.Client", *filters: Filter):
        """Decorator for unconfirmed session updates (anti-login)."""
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

            self.add_handler(wrapper, handlers.UnconfirmedSessionUpdates())
            return func
        return MetaHandler