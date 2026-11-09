from typing import Optional, Dict, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

KeepMediaType = Literal['Forever']

class SetDataSetting:
    async def set_data_setting(
        self: "maxrubika.Messenger",
        auto_download_media: Optional[bool] = None,
        wifi_auto_download: Optional[bool] = None,
        cellular_auto_download: Optional[bool] = None,
        gif_auto_play: Optional[bool] = None,
        video_auto_play: Optional[bool] = None,
        stream_videos_and_audio_files: Optional[bool] = None,
        keep_media: Optional[KeepMediaType] = None,
        wifi_photo_auto_download: Optional[Dict[str, int]] = None,
        cellular_photo_auto_download: Optional[Dict[str, int]] = None,
        wifi_video_auto_download: Optional[Dict[str, int]] = None,
        cellular_video_auto_download: Optional[Dict[str, int]] = None,
        wifi_file_auto_download: Optional[Dict[str, int]] = None,
        cellular_file_auto_download: Optional[Dict[str, int]] = None,
        wifi_gif_auto_download: Optional[Dict[str, int]] = None,
        cellular_gif_auto_download: Optional[Dict[str, int]] = None,
        wifi_music_auto_download: Optional[Dict[str, int]] = None,
        cellular_music_auto_download: Optional[Dict[str, int]] = None,
    ):
        """
        Update data (auto-download) settings.

        Parameters:
            auto_download_media (bool, optional): Global auto-download toggle.
            wifi_auto_download (bool, optional): WiFi auto-download toggle.
            cellular_auto_download (bool, optional): Cellular auto-download toggle.
            gif_auto_play (bool, optional): Auto-play GIFs.
            video_auto_play (bool, optional): Auto-play videos.
            stream_videos_and_audio_files (bool, optional): Stream videos and audio.
            keep_media (str, optional): Keep media duration. Only 'Forever' is accepted.
            wifi_photo_auto_download (dict, optional): Auto-download config with 'max_download_size' and contact/user/group/channel keys.
            cellular_photo_auto_download (dict, optional): Same as above for cellular.
            wifi_video_auto_download (dict, optional): Same as above for video on WiFi.
            cellular_video_auto_download (dict, optional): Same as above for video on cellular.
            wifi_file_auto_download (dict, optional): Same as above for files on WiFi.
            cellular_file_auto_download (dict, optional): Same as above for files on cellular.
            wifi_gif_auto_download (dict, optional): Same as above for GIFs on WiFi.
            cellular_gif_auto_download (dict, optional): Same as above for GIFs on cellular.
            wifi_music_auto_download (dict, optional): Same as above for music on WiFi.
            cellular_music_auto_download (dict, optional): Same as above for music on cellular.

        Returns:
            The updated device settings.
        """
        from ...exceptions import InvalidInput

        settings = {}
        update_parameters = []

        simple_params = {
            'auto_download_media': auto_download_media,
            'wifi_auto_download': wifi_auto_download,
            'cellular_auto_download': cellular_auto_download,
            'gif_auto_play': gif_auto_play,
            'video_auto_play': video_auto_play,
            'stream_videos_and_audio_files': stream_videos_and_audio_files,
        }
        for key, value in simple_params.items():
            if value is not None:
                settings[key] = value
                update_parameters.append(key)

        if keep_media is not None:
            if keep_media != 'Forever':
                raise InvalidInput("'keep_media' must be 'Forever'.")
            settings['keep_media'] = keep_media
            update_parameters.append('keep_media')

        auto_download_params = {
            'wifi_photo_auto_download': wifi_photo_auto_download,
            'cellular_photo_auto_download': cellular_photo_auto_download,
            'wifi_video_auto_download': wifi_video_auto_download,
            'cellular_video_auto_download': cellular_video_auto_download,
            'wifi_file_auto_download': wifi_file_auto_download,
            'cellular_file_auto_download': cellular_file_auto_download,
            'wifi_gif_auto_download': wifi_gif_auto_download,
            'cellular_gif_auto_download': cellular_gif_auto_download,
            'wifi_music_auto_download': wifi_music_auto_download,
            'cellular_music_auto_download': cellular_music_auto_download,
        }

        for key, value in auto_download_params.items():
            if value is not None:
                if not isinstance(value, dict):
                    message = f"'{key}' must be a dict."
                    raise InvalidInput(message)
                if 'max_download_size' not in value:
                    message = f"'{key}' must include 'max_download_size'."
                    raise InvalidInput(message)
                settings[key] = value
                update_parameters.append(key)

        if not settings:
            raise InvalidInput("At least one data setting must be provided.")

        input_data = {
            'settings': settings,
            'update_parameters': update_parameters
        }

        await self.request(method='setSetting', input=input_data)

        return await self.get_data_setting()