from ..hybrid import wrap_methods

from .accept_follow_request import AcceptFollowRequest
from .accept_message_owner import AcceptMessageOwner
from .accept_profile_admin import AcceptProfileAdmin
from .add_impression_ids import AddImpressionIDs
from .add_post import AddPost
from .add_post_comment import AddPostComment
from .add_story import AddStory
from .add_usage_time import AddUsageTime
from .block_profile import BlockProfile
from .create_page import CreatePage
from .delete_page import DeletePage
from .delete_page_avatar import DeletePageAvatar
from .delete_post import DeletePost
from .delete_post_comment import DeletePostComment
from .delete_story import DeleteStory
from .deny_message_owner import DenyMessageOwner
from .deny_profile_admin import DenyProfileAdmin
from .download_post import DownloadPost
from .download_story import DownloadStory
from .follow_page import FollowPage
from .get_blocked_profiles import GetBlockedProfiles
from .get_boost_url import GetBoostUrl
from .get_events import GetEvents
from .get_explore_post_topics import GetExplorePostTopics
from .get_explore_posts import GetExplorePosts
from .get_feed_data import GetFeedData
from .get_follow_requests import GetFollowRequests
from .get_info_by_username import GetInfoByUsername
from .get_me import GetMe
from .get_metrics_config import GetMetricsConfig
from .get_my_close_friends import GetMyCloseFriends
from .get_my_profile_id import GetMyProfileID
from .get_my_profile_settings import GetMyProfileSettings
from .get_post_by_link import GetPostByLink
from .get_post_comment_likes import GetPostCommentLikes
from .get_post_comments import GetPostComments
from .get_post_id import GetPostID
from .get_post_likes import GetPostLikes
from .get_post_link import GetPostLink
from .get_posts_by_hashtag import GetPostsByHashtag
from .get_posts_by_ids import GetPostsByIDs
from .get_profile_admins import GetProfileAdmins
from .get_profile_followers import GetProfileFollowers
from .get_profile_followings import GetProfileFollowings
from .get_profile_id import GetProfileID
from .get_profile_info import GetProfileInfo
from .get_profile_posts import GetProfilePosts
from .get_profile_stories import GetProfileStories
from .get_related_posts import GetRelatedPosts
from .get_saved_posts import GetSavedPosts
from .get_setting_admin_permissions import GetSettingAdminPermissions
from .get_story_viewers import GetStoryViewers
from .get_suggested_profiles import GetSuggestedProfiles
from .hide_post_comment import HidePostComment
from .like_post import LikePost
from .like_post_comment import LikePostComment
from .not_interested_profile import NotInterestedProfile
from .pin_post_comment import PinPostComment
from .post_collaborator_action import PostCollaboratorAction
from .profile_created_at import ProfileCreatedAt
from .reject_follow_request import RejectFollowRequest
from .remove_follower import RemoveFollower
from .remove_message_owner import RemoveMessageOwner
from .remove_profile_admin import RemoveProfileAdmin
from .report_comment import ReportComment
from .report_hashtag import ReportHashtag
from .report_live import ReportLive
from .report_post import ReportPost
from .report_profile import ReportProfile
from .report_story import ReportStory
from .request import Request
from .request_send_file import RequestSendFile
from .save_post import SavePost
from .search_hashtag import SearchHashtag
from .search_location import SearchLocation
from .search_post import SearchPost
from .search_profile import SearchProfile
from .set_close_friends import SetCloseFriends
from .set_page_avatar import SetPageAvatar
from .set_post_feedback import SetPostFeedback
from .set_profile_admin import SetProfileAdmin
from .set_profile_setting import SetProfileSetting
from .set_profile_status import SetProfileStatus
from .set_profile_type import SetProfileType
from .track_client_metrics import TrackClientMetrics
from .unblock_profile import UnblockProfile
from .unfollow_page import UnfollowPage
from .unhide_post_comment import UnhidePostComment
from .unlike_post import UnlikePost
from .unlike_post_comment import UnlikePostComment
from .unpin_post_comment import UnpinPostComment
from .unsave_post import UnsavePost
from .unset_close_friends import UnsetCloseFriends
from .unset_profile_admin import UnsetProfileAdmin
from .update_page import UpdatePage
from .update_post import UpdatePost
from .update_post_share_count import UpdatePostShareCount
from .upload_file import UploadFile
from .view_feed_data import ViewFeedData
from .view_post import ViewPost
from .view_story import ViewStory

class Methods(
    AcceptFollowRequest,
    AcceptMessageOwner,
    AcceptProfileAdmin,
    AddImpressionIDs,
    AddPost,
    AddPostComment,
    AddStory,
    AddUsageTime,
    BlockProfile,
    CreatePage,
    DeletePage,
    DeletePageAvatar,
    DeletePost,
    DeletePostComment,
    DeleteStory,
    DenyMessageOwner,
    DenyProfileAdmin,
    DownloadPost,
    DownloadStory,
    FollowPage,
    GetBlockedProfiles,
    GetBoostUrl,
    GetEvents,
    GetExplorePostTopics,
    GetExplorePosts,
    GetFeedData,
    GetFollowRequests,
    GetInfoByUsername,
    GetMe,
    GetMetricsConfig,
    GetMyCloseFriends,
    GetMyProfileID,
    GetMyProfileSettings,
    GetPostByLink,
    GetPostCommentLikes,
    GetPostComments,
    GetPostID,
    GetPostLikes,
    GetPostLink,
    GetPostsByHashtag,
    GetPostsByIDs,
    GetProfileAdmins,
    GetProfileFollowers,
    GetProfileFollowings,
    GetProfileID,
    GetProfileInfo,
    GetProfilePosts,
    GetProfileStories,
    GetRelatedPosts,
    GetSavedPosts,
    GetSettingAdminPermissions,
    GetStoryViewers,
    GetSuggestedProfiles,
    HidePostComment,
    LikePost,
    LikePostComment,
    NotInterestedProfile,
    PinPostComment,
    PostCollaboratorAction,
    ProfileCreatedAt,
    RejectFollowRequest,
    RemoveFollower,
    RemoveMessageOwner,
    RemoveProfileAdmin,
    ReportComment,
    ReportHashtag,
    ReportLive,
    ReportPost,
    ReportProfile,
    ReportStory,
    Request,
    RequestSendFile,
    SavePost,
    SearchHashtag,
    SearchLocation,
    SearchPost,
    SearchProfile,
    SetCloseFriends,
    SetPageAvatar,
    SetPostFeedback,
    SetProfileAdmin,
    SetProfileSetting,
    SetProfileStatus,
    SetProfileType,
    TrackClientMetrics,
    UnblockProfile,
    UnfollowPage,
    UnhidePostComment,
    UnlikePost,
    UnlikePostComment,
    UnpinPostComment,
    UnsavePost,
    UnsetCloseFriends,
    UnsetProfileAdmin,
    UpdatePage,
    UpdatePost,
    UpdatePostShareCount,
    UploadFile,
    ViewFeedData,
    ViewPost,
    ViewStory
):
    pass

wrap_methods(Methods)