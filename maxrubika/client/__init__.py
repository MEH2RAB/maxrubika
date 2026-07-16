from ..hybrid import wrap_methods

from . import exceptions, filters, enums
from .base import Base
from .bots import Bots
from .channels import Channels
from .chats import Chats
from .core import Core
from .decorators import Decorators
from .extras import Exctras
from .groups import Groups
from .messages import Messages
from .settings import Settings
from .users import Users

class Methods(
    Base,
    Bots,
    Channels,
    Chats,
    Core,
    Decorators,
    Exctras,
    Groups,
    Messages,
    Settings,
    Users
):
    pass

wrap_methods(Methods)