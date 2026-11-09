from .archive_chat import ArchiveChat
from .delete_all_avatars import DeleteAllAvatars
from .delete_avatar import DeleteAvatar
from .delete_chat_history import DeleteChatHistory
from .get_avatars import GetAvatars
from .mute_chat import MuteChat
from .pin_chat import PinChat
from .pin_chat_in_folder import PinChatInFolder
from .set_ask_spam import SetAskSpam
from .set_avatar_as_main import SetAvatarAsMain
from .set_chat_auto_delete import SetChatAutoDelete
from .set_chat_protected_content import SetChatProtectedContent
from .unarchive_chat import UnarchiveChat
from .unmute_chat import UnmuteChat
from .unpin_chat import UnpinChat
from .unpin_chat_in_folder import UnpinChatInFolder
from .upload_avatar import UploadAvatar

class Settings(
    ArchiveChat,
    DeleteAllAvatars,
    DeleteAvatar,
    DeleteChatHistory,
    GetAvatars,
    MuteChat,
    PinChat,
    PinChatInFolder,
    SetAskSpam,
    SetAvatarAsMain,
    SetChatAutoDelete,
    SetChatProtectedContent,
    UnarchiveChat,
    UnmuteChat,
    UnpinChat,
    UnpinChatInFolder,
    UploadAvatar
):
    pass