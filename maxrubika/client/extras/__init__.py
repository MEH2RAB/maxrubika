from .add_live_comment import AddLiveComment
from .add_sticker_set import AddStickerSet
from .add_to_my_gif_set import AddToMyGifSet
from .delete_my_gif_set import DeleteMyGifSet
from .delete_sticker_set import DeleteStickerSet
from .feedback_voice_transcription import FeedbackVoiceTranscription
from .get_available_reactions import GetAvailableReactions
from .get_live_comments import GetLiveComments
from .get_live_play_url import GetLivePlayUrl
from .get_live_status import GetLiveStatus
from .get_location_view import GetLocationView
from .get_my_archived_sticker_sets import GetMyArchivedStickerSets
from .get_my_gif_set import GetMyGifSet
from .get_my_sticker_sets import GetMyStickerSets
from .get_sticker_set_by_id import GetStickerSetByID
from .get_sticker_setting import GetStickerSetting
from .get_stickers_by_emoji import GetStickersByEmoji
from .get_stickers_by_set_ids import GetStickersBySetIDs
from .get_time import GetTime
from .get_trend_sticker_sets import GetTrendStickerSets
from .get_wallpapers import GetWallpapers
from .reset_wallpapers import ResetWallpapers
from .search_stickers import SearchStickers

class Exctras(
    AddLiveComment,
    AddStickerSet,
    AddToMyGifSet,
    DeleteMyGifSet,
    DeleteStickerSet,
    FeedbackVoiceTranscription,
    GetAvailableReactions,
    GetLiveComments,
    GetLivePlayUrl,
    GetLiveStatus,
    GetLocationView,
    GetMyArchivedStickerSets,
    GetMyGifSet,
    GetMyStickerSets,
    GetStickerSetByID,
    GetStickerSetting,
    GetStickersByEmoji,
    GetStickersBySetIDs,
    GetTime,
    GetTrendStickerSets,
    GetWallpapers,
    ResetWallpapers,
    SearchStickers
):
    pass