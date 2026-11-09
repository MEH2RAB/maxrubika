from .accept_call import AcceptCall
from .add_contact import AddContact
from .block_user import BlockUser
from .call_started import CallStarted
from .check_user_username import CheckUserUsername
from .delete_contact import DeleteContact
from .delete_user_chat import DeleteUserChat
from .discard_call import DiscardCall
from .get_blocked_users import GetBlockedUsers
from .get_call_config import GetCallConfig
from .get_call_signaling_data import GetCallSignalingData
from .get_calls import GetCalls
from .get_common_groups import GetCommonGroups
from .get_contacts import GetContacts
from .get_contacts_last_online import GetContactsLastOnline
from .get_contacts_stories import GetContactsStories
from .get_contacts_updates import GetContactsUpdates
from .get_last_online import GetLastOnline
from .get_me import GetMe
from .get_saved_music_playlist import GetSavedMusicPlaylist
from .get_top_users import GetTopUsers
from .get_user_info import GetUserInfo
from .import_contacts import ImportContacts
from .rate_call import RateCall
from .received_call import ReceivedCall
from .remove_from_top_users import RemoveFromTopUsers
from .request_video_call import RequestVideoCall
from .request_voice_call import RequestVoiceCall
from .reset_contacts import ResetContacts
from .send_call_signaling_data import SendCallSignalingData
from .unblock_all_users import UnblockAllUsers
from .unblock_user import UnblockUser

class Users(
    AcceptCall,
    AddContact,
    BlockUser,
    CallStarted,
    CheckUserUsername,
    DeleteContact,
    DeleteUserChat,
    DiscardCall,
    GetBlockedUsers,
    GetCallConfig,
    GetCallSignalingData,
    GetCalls,
    GetCommonGroups,
    GetContacts,
    GetContactsLastOnline,
    GetContactsStories,
    GetContactsUpdates,
    GetLastOnline,
    GetMe,
    GetSavedMusicPlaylist,
    GetTopUsers,
    GetUserInfo,
    ImportContacts,
    RateCall,
    ReceivedCall,
    RemoveFromTopUsers,
    RequestVideoCall,
    RequestVoiceCall,
    ResetContacts,
    SendCallSignalingData,
    UnblockAllUsers,
    UnblockUser
):
    pass