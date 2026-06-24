from ..hybrid import wrap_methods

from .auto_delete_message import AutoDeleteMessage
from .ban_member import BanMember
from .delete_message import DeleteMessage
from .download_file import DownloadFile
from .edit_chat_keypad import EditChatKeypad
from .edit_inline_keypad import EditInlineKeypad
from .edit_message import EditMessage
from .forward_message import ForwardMessage
from .get_chat_info import GetChatInfo
from .get_file import GetFile
from .get_me import GetMe
from .get_updates import GetUpdates
from .register_all_endpoints import RegisterAllEndpoints
from .remove_chat_keypad import RemoveChatKeypad
from .remove_member import RemoveMember
from .request_send_file import RequestSendFile
from .run import Run
from .send_contact import SendContact
from .send_file import SendFile
from .send_gif import SendGif
from .send_image import SendImage
from .send_location import Sendlocation
from .send_message import SendMessage
from .send_music import SendMusic
from .send_poll import SendPoll
from .send_quiz import SendQuiz
from .send_video import SendVideo
from .send_voice import SendVoice
from .set_commands import SetCommands
from .start import Start
from .unban_member import UnbanMember
from .update_bot_endpoints import UpdateBotEndpoints
from .upload_file import UploadFile

class Methods(
    AutoDeleteMessage,
    BanMember,
    DeleteMessage,
    DownloadFile,
    EditChatKeypad,
    EditInlineKeypad,
    EditMessage,
    ForwardMessage,
    GetChatInfo,
    GetFile,
    GetMe,
    GetUpdates,
    RegisterAllEndpoints,
    RemoveChatKeypad,
    RemoveMember,
    RequestSendFile,
    Run,
    SendContact,
    SendFile,
    SendGif,
    SendImage,
    Sendlocation,
    SendMessage,
    SendMusic,
    SendPoll,
    SendQuiz,
    SendVideo,
    SendVoice,
    SetCommands,
    Start,
    UnbanMember,
    UpdateBotEndpoints,
    UploadFile,
):
    pass

wrap_methods(Methods)