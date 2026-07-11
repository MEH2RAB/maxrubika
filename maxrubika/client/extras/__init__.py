from .add_live_comment import AddLiveComment
from .add_sticker_set import AddStickerSet
from .add_to_my_gif_set import AddToMyGifSet
from .delete_my_gif_set import DeleteMyGifSet
from .delete_sticker_set import DeleteStickerSet
from .get_available_reactions import GetAvailableReactions
from .get_live_comments import GetLiveComments
from .get_live_play_url import GetLivePlayUrl
from .get_live_status import GetLiveStatus
from .get_location_view import GetLocationView
from .get_my_gif_set import GetMyGifSet
from .get_my_sticker_sets import GetMyStickerSets
from .get_sticker_set_by_id import GetStickerSetByID
from .get_stickers_by_emoji import GetStickersByEmoji
from .get_stickers_by_set_ids import GetStickersBySetIDs
from .get_time import GetTime
from .get_trend_sticker_sets import GetTrendStickerSets
from .search_stickers import SearchStickers

class Exctras(
    AddLiveComment,
    AddStickerSet,
    AddToMyGifSet,
    DeleteMyGifSet,
    DeleteStickerSet,
    GetAvailableReactions,
    GetLiveComments,
    GetLivePlayUrl,
    GetLiveStatus,
    GetLocationView,
    GetMyGifSet,
    GetMyStickerSets,
    GetStickerSetByID,
    GetStickersByEmoji,
    GetStickersBySetIDs,
    GetTime,
    GetTrendStickerSets,
    SearchStickers
):
    pass