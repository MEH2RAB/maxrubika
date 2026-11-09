from .add_saved_music_playlist import AddSavedMusicPlaylist
from .add_saved_music_track import AddSavedMusicTrack
from .delete_saved_music_playlist import DeleteSavedMusicPlaylist
from .get_appearance_setting import GetAppearanceSetting
from .get_data_setting import GetDataSetting
from .get_device_setting import GetDeviceSetting
from .get_notification_setting import GetNotificationSetting
from .logout import Logout
from .set_appearance_setting import SetAppearanceSetting
from .set_data_setting import SetDataSetting
from .set_notification import SetNotification
from .set_notification_setting import SetNotificationSetting
from .set_quick_reaction import SetQuickReaction
from .set_saved_music_playlist import SetSavedMusicPlaylist
from .set_theme import SetTheme
from .set_theme_background import SetThemeBackground
from .upload_wallpaper import UploadWallpaper

class General(
    AddSavedMusicPlaylist,
    AddSavedMusicTrack,
    DeleteSavedMusicPlaylist,
    GetAppearanceSetting,
    GetDataSetting,
    GetDeviceSetting,
    GetNotificationSetting,
    Logout,
    SetAppearanceSetting,
    SetDataSetting,
    SetNotification,
    SetNotificationSetting,
    SetQuickReaction,
    SetSavedMusicPlaylist,
    SetTheme,
    SetThemeBackground,
    UploadWallpaper
):
    pass