from .clear_all_drafts import ClearAllDrafts
from .clear_chat_draft import ClearChatDraft
from .click_chat_ads import ClickChatAds
from .click_keypad_button import ClickKeypadButton
from .dont_show_chat_ads import DontShowChatAds
from .download_avatars import DownloadAvatars
from .download_profile_picture import DownloadProfilePicture
from .get_all_drafts import GetAllDrafts
from .report_chat import ReportChat
from .report_chat_ads import ReportChatAds
from .seen_chats import SeenChats
from .send_chat_activity import SendChatActivity
from .set_chat_use_time import SetChatUseTime
from .view_chat_ads import ViewChatAds

class Utilities(
    ClearAllDrafts,
    ClearChatDraft,
    ClickChatAds,
    ClickKeypadButton,
    DontShowChatAds,
    DownloadAvatars,
    DownloadProfilePicture,
    GetAllDrafts,
    ReportChat,
    ReportChatAds,
    SeenChats,
    SendChatActivity,
    SetChatUseTime,
    ViewChatAds
):
    pass