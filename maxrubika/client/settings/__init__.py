from .account import Account
from .folders import Folders
from .general import General
from .privacy import Privacy
from .security import Security

class Settings(
    Account,
    Folders,
    General,
    Privacy,
    Security
):
    pass