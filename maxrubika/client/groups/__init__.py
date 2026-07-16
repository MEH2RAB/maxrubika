from .create_group import CreateGroup
from .delete_group import DeleteGroup
from .edit_group_info import EditGroupInfo
from .edit_group_timer import EditGroupTimer
from .edit_group_title import EditGroupTitle
from .edit_slow_mode import EditSlowMode
from .get_group_admin_access import GetGroupAdminAccess
from .get_group_admins import GetGroupAdmins
from .get_group_default_access import GetGroupDefaultAccess
from .get_group_info import GetGroupInfo
from .get_group_link import GetGroupLink
from .get_group_members import GetGroupMembers
from .get_group_mention_list import GetGroupMentionList
from .get_group_message_read_participants import GetGroupMessageReadParticipants
from .get_group_online_count import GetGroupOnlineCount
from .get_unread_mentions import GetUnreadMentions
from .join_group import JoinGroup
from .leave_group import LeaveGroup
from .lock_group import LockGroup
from .set_group_default_access import SetGroupDefaultAccess
from .set_group_link import SetGroupLink
from .unlock_group import UnlockGroup

class Groups(
    CreateGroup,
    DeleteGroup,
    EditGroupInfo,
    EditGroupTimer,
    EditGroupTitle,
    EditSlowMode,
    GetGroupAdminAccess,
    GetGroupAdmins,
    GetGroupDefaultAccess,
    GetGroupInfo,
    GetGroupLink,
    GetGroupMembers,
    GetGroupMentionList,
    GetGroupMessageReadParticipants,
    GetGroupOnlineCount,
    GetUnreadMentions,
    JoinGroup,
    LeaveGroup,
    LockGroup,
    SetGroupDefaultAccess,
    SetGroupLink,
    UnlockGroup
):
    pass