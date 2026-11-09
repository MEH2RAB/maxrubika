from .check_rubino_username import CheckRubinoUsername
from .get_abs_chats import GetAbsChats
from .get_chat_ads import GetChatAds
from .get_chat_info import GetChatInfo
from .get_chats import GetChats
from .get_chats_info import GetChatsInfo
from .get_chats_updates import GetChatsUpdates
from .get_guid import GetGuid
from .get_info_by_link import GetInfoByLink
from .get_info_by_username import GetInfoByUsername
from .get_my_guid import GetMyGuid
from .get_profile_link_items import GetProfileLinkItems
from .get_related_chats import GetRelatedChats
from .search_global_chats import SearchGlobalChats

class Information(
    CheckRubinoUsername,
    GetAbsChats,
    GetChatAds,
    GetChatInfo,
    GetChats,
    GetChatsInfo,
    GetChatsUpdates,
    GetGuid,
    GetInfoByLink,
    GetInfoByUsername,
    GetMyGuid,
    GetProfileLinkItems,
    GetRelatedChats,
    SearchGlobalChats
):
    pass