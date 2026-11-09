from .check_voice_chat_participants import CheckVoiceChatParticipants
from .discard_voice_chat import DiscardVoiceChat
from .get_chat_voice_chat import GetChatVoiceChat
from .get_voice_chat_participants import GetVoiceChatParticipants
from .get_voice_chat_updates import GetVoiceChatUpdates
from .invite_to_voice_chat import InviteToVoiceChat
from .join_voice_chat import JoinVoiceChat
from .leave_voice_chat import LeaveVoiceChat
from .play_voice_chat import PlayVoiceChat
from .send_voice_chat_activity import SendVoiceChatActivity
from .set_voice_chat_setting import SetVoiceChatSetting
from .set_voice_chat_state import SetVoiceChatState
from .start_voice_chat import StartVoiceChat

class VoiceChat(
    CheckVoiceChatParticipants,
    DiscardVoiceChat,
    GetChatVoiceChat,
    GetVoiceChatParticipants,
    GetVoiceChatUpdates,
    InviteToVoiceChat,
    JoinVoiceChat,
    LeaveVoiceChat,
    PlayVoiceChat,
    SendVoiceChatActivity,
    SetVoiceChatSetting,
    SetVoiceChatState,
    StartVoiceChat
):
    pass