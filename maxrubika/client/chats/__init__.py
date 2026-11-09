from .information import Information
from .management import Management
from .members import Members
from .settings import Settings
from .utilities import Utilities
from .voice_chat import VoiceChat

class Chats(
    Information,
    Management,
    Members,
    Settings,
    Utilities,
    VoiceChat
):
    pass