from .add_contact import AddContact
from .block_user import BlockUser
from .check_user_username import CheckUserUsername
from .delete_contact import DeleteContact
from .delete_user_chat import DeleteUserChat
from .discard_call import DiscardCall
from .get_blocked_users import GetBlockedUsers
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
from .remove_from_top_users import RemoveFromTopUsers
from .request_video_call import RequestVideoCall
from .request_voice_call import RequestVoiceCall
from .reset_contacts import ResetContacts
from .unblock_all_users import UnblockAllUsers
from .unblock_user import UnblockUser

class Users(
    AddContact,
    BlockUser,
    CheckUserUsername,
    DeleteContact,
    DeleteUserChat,
    DiscardCall,
    GetBlockedUsers,
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
    RemoveFromTopUsers,
    RequestVideoCall,
    RequestVoiceCall,
    ResetContacts,
    UnblockAllUsers,
    UnblockUser

):
    pass