from .accept_ownership_request import AcceptOwnershipRequest
from .add_member import AddMember
from .add_members import AddMembers
from .ban_member import BanMember
from .ban_members import BanMembers
from .cancel_change_owner import CancelChangeOwner
from .change_owner import ChangeOwner
from .clear_black_list import ClearBlackList
from .get_banned_members import GetBannedMembers
from .get_pending_owner import GetPendingOwner
from .member_is_admin import MemberIsAdmin
from .member_is_joined import MemberIsJoined
from .member_is_owner import MemberIsOwner
from .reject_ownership_request import RejectOwnershipRequest
from .set_admin import SetAdmin
from .unban_all_members import UnbanAllMembers
from .unban_member import UnbanMember
from .unban_members import UnbanMembers
from .unset_admin import UnsetAdmin

class Members(
    AcceptOwnershipRequest,
    AddMember,
    AddMembers,
    BanMember,
    BanMembers,
    CancelChangeOwner,
    ChangeOwner,
    ClearBlackList,
    GetBannedMembers,
    GetPendingOwner,
    MemberIsAdmin,
    MemberIsJoined,
    MemberIsOwner,
    RejectOwnershipRequest,
    SetAdmin,
    UnbanAllMembers,
    UnbanMember,
    UnbanMembers,
    UnsetAdmin
):
    pass