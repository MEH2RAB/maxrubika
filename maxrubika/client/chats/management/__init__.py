from .accept_all_join_requests import AcceptAllJoinRequests
from .accept_join_request import AcceptJoinRequest
from .check_join import CheckJoin
from .create_join_link import CreateJoinLink
from .delete_revoked_join_link import DeleteRevokedJoinLink
from .delete_revoked_join_links import DeleteRevokedJoinLinks
from .edit_join_link import EditJoinLink
from .get_join_link_user_joined import GetJoinLinkUserJoined
from .get_join_links import GetJoinLinks
from .get_join_requests import GetJoinRequests
from .join_chat import JoinChat
from .leave_chat import LeaveChat
from .reject_join_request import RejectJoinRequest
from .revoke_join_link import RevokeJoinLink

class Management(
    AcceptAllJoinRequests,
    AcceptJoinRequest,
    CheckJoin,
    CreateJoinLink,
    DeleteRevokedJoinLink,
    DeleteRevokedJoinLinks,
    EditJoinLink,
    GetJoinLinkUserJoined,
    GetJoinLinks,
    GetJoinRequests,
    JoinChat,
    LeaveChat,
    RejectJoinRequest,
    RevokeJoinLink
):
    pass