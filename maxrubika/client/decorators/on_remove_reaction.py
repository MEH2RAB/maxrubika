import maxrubika
from ..core import handlers
from ..filters import Filter

class OnRemoveReaction:
    def on_remove_reaction(self: "maxrubika.Client", *filters: Filter):
        """Decorator for reaction removed."""
        def MetaHandler(func):
            async def wrapper(event):
                if hasattr(event, 'original_data'):
                    data = event.original_data
                else:
                    return

                action = data.get('action')
                updated = data.get('updated_parameters', [])
                msg = data.get('message', {})
                reactions = msg.get('reactions', []) if isinstance(msg, dict) else []

                if not (action == "Edit" and "reactions" in updated and not reactions):
                    return

                for f in filters:
                    if hasattr(f, 'evaluate'):
                        if not await f.evaluate(event):
                            return

                return await func(event)

            handler = handlers.MessageUpdates()
            self.add_handler(wrapper, handler)
            return func
        return MetaHandler