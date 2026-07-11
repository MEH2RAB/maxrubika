import asyncio
import sys
from typing import Type, List, Dict, Any, Optional
from ...data import Data

AUTHORIZED_HANDLERS = [
    "ChatUpdates",
    "MessageUpdates",
    "ShowActivities",
    "ShowNotifications",
    "RemoveNotifications",
]

def create_handler(
    name: str,
    base: tuple,
    authorized_handlers: List[str] = AUTHORIZED_HANDLERS,
    exception: bool = True,
    **kwargs,
) -> Optional[Type["BaseHandlers"]]:
    if name in authorized_handlers:
        return type(name, base, {"__name__": name, **kwargs})

    if not exception:
        return None

    raise AttributeError(f"Module has no handler named '{name}'")

class BaseHandlers(Data):
    __name__ = "CustomHandlers"

    def __init__(self, *filters: Any, any_handler: bool = False, **kwargs) -> None:
        self._filters = filters
        self.__any_handler = any_handler

    async def __call__(self, event: Dict, *args, **kwargs) -> bool:
        self.original_event = event

        if not self._filters:
            return True

        for f in self._filters:
            if hasattr(f, 'evaluate'):
                if not await f.evaluate(event):
                    return False
            else:
                if not f:
                    return False

        return True

class Handlers:
    def __init__(self, name: str) -> None:
        self.__name__ = name

    def __eq__(self, value: object) -> bool:
        return BaseHandlers in getattr(value, "__bases__", ())

    def __dir__(self) -> List[str]:
        return sorted(AUTHORIZED_HANDLERS)

    def __call__(self, name: str, *args, **kwargs) -> Type["BaseHandlers"]:
        return self.__getattr__(name)(*args, **kwargs)

    def __getattr__(self, name: str) -> Type["BaseHandlers"]:
        return create_handler(name, (BaseHandlers,), AUTHORIZED_HANDLERS)

sys.modules[__name__] = Handlers(__name__)

ChatUpdates: Type[BaseHandlers]
MessageUpdates: Type[BaseHandlers]
ShowActivities: Type[BaseHandlers]
ShowNotifications: Type[BaseHandlers]
RemoveNotifications: Type[BaseHandlers]