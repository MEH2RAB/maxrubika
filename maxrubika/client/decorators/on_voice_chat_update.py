import maxrubika
from ..core import handlers
from ..filters import Filter

class OnVoiceChatUpdate:
    def on_voice_chat_update(self: "maxrubika.Client", *filters: Filter):
        """Decorator for voice chat updates."""
        def MetaHandler(func):
            async def wrapper(event):
                for f in filters:
                    if hasattr(f, 'evaluate'):
                        if not await f.evaluate(event):
                            return
                return await func(event)
            self.add_handler(wrapper, handlers.GroupVoiceChatUpdates())
            return func
        return MetaHandler