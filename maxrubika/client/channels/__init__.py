from .check_channel_username import CheckChannelUsername
from .create_channel import CreateChannel
from .delete_channel import DeleteChannel
from .edit_channel_info import EditChannelInfo
from .edit_channel_title import EditChannelTitle
from .get_channel_admin_access import GetChannelAdminAccess
from .get_channel_admins import GetChannelAdmins
from .get_channel_info import GetChannelInfo
from .get_channel_link import GetChannelLink
from .get_channel_members import GetChannelMembers
from .get_channel_post_by_link import GetChannelPostByLink
from .get_channel_seen_count import GetChannelSeenCount
from .get_channel_statistics import GetChannelStatistics
from .join_channel import JoinChannel
from .leave_channel import LeaveChannel
from .seen_channel_messages import SeenChannelMessages
from .set_channel_link import SetChannelLink
from .set_channel_type import SetChannelType
from .update_channel_username import UpdateChannelUsername

class Channels(
    CheckChannelUsername,
    CreateChannel,
    DeleteChannel,
    EditChannelInfo,
    EditChannelTitle,
    GetChannelAdminAccess,
    GetChannelAdmins,
    GetChannelInfo,
    GetChannelLink,
    GetChannelMembers,
    GetChannelPostByLink,
    GetChannelSeenCount,
    GetChannelStatistics,
    JoinChannel,
    LeaveChannel,
    SeenChannelMessages,
    SetChannelLink,
    SetChannelType,
    UpdateChannelUsername
):
    pass