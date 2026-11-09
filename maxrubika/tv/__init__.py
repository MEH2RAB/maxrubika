from ..hybrid import wrap_methods

from .add_wish_media import AddWishMedia
from .dislike_media import DislikeMedia
from .follow_media import FollowMedia
from .get_cast_details import GetCastDetails
from .get_cast_medias import GetCastMedias
from .get_custom_menu_items import GetCustomMenuItems
from .get_list_items import GetListItems
from .get_listing import GetListing
from .get_media import GetMedia
from .get_media_by_link import GetMediaByLink
from .get_media_related import GetMediaRelated
from .get_me import GetMe
from .get_next_episode import GetNextEpisode
from .get_next_media_info import GetNextMediaInfo
from .get_play_info import GetPlayInfo
from .get_play_suggested_episode import GetPlaySuggestedEpisode
from .get_property_types import GetPropertyTypes
from .get_season_episodes import GetSeasonEpisodes
from .get_wish_list import GetWishList
from .like_media import LikeMedia
from .remove_wish_list_media import RemoveWishListMedia
from .request import Request
from .search_movie import SearchMovie
from .set_current_play_time import SetCurrentPlayTime
from .set_session_play_duration import SetSessionPlayDuration
from .undo_like_or_dislike_media import UndoLikeOrDislikeMedia
from .unfollow_media import UnFollowMedia
from .view_commercial import ViewCommercial

class Methods(
    AddWishMedia,
    DislikeMedia,
    FollowMedia,
    GetCastDetails,
    GetCastMedias,
    GetCustomMenuItems,
    GetListItems,
    GetListing,
    GetMedia,
    GetMediaByLink,
    GetMediaRelated,
    GetMe,
    GetNextEpisode,
    GetNextMediaInfo,
    GetPlayInfo,
    GetPlaySuggestedEpisode,
    GetPropertyTypes,
    GetSeasonEpisodes,
    GetWishList,
    LikeMedia,
    RemoveWishListMedia,
    Request,
    SearchMovie,
    SetCurrentPlayTime,
    SetSessionPlayDuration,
    UndoLikeOrDislikeMedia,
    UnFollowMedia,
    ViewCommercial
):
    pass

wrap_methods(Methods)