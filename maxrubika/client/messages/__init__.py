from .actions import Actions
from .fetch import Fetch
from .send import Send
from .utilities import Utilities

class Messages(
    Actions,
    Fetch,
    Send,
    Utilities
):
    pass