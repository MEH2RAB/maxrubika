import inspect
from typing import TYPE_CHECKING

from ..core import handlers
from ..filters import Filter

if TYPE_CHECKING:
    import maxrubika

class OnVoiceChatUpdate:
    def on_voice_chat_update(self: "maxrubika.Messenger", *filters: Filter):
        """Decorator for voice chat updates."""
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

            self.add_handler(wrapper, handlers.GroupVoiceChatUpdates())
            return func
        return MetaHandler