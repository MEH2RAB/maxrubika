import inspect
import maxrubika
from ..core import handlers
from ..filters import Filter

class OnVoiceChatParticipant:
    def on_voice_chat_participant(self: "maxrubika.Client", *filters: Filter):
        """Decorator for voice chat participant updates."""
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

            self.add_handler(wrapper, handlers.GroupVoiceChatParticipantUpdates())
            return func
        return MetaHandler