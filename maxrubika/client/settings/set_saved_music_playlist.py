from typing import Union, List
from pathlib import Path
import maxrubika
from ..core import media

class SetSavedMusicPlaylist:
    async def set_saved_music_playlist(
        self: "maxrubika.Client",
        files: Union[Path, str, List[Union[Path, str]]]
    ):
        """
        Set the saved music playlist on your profile.

        Parameters:
            files (Union[Path, str, List[Union[Path, str]]]): 
                A single file path or a list of file paths to music files.

        Returns:
            The result of the API call.
        """
        if isinstance(files, (str, Path)):
            files = [files]

        try:
            current = await self.get_saved_music_playlist(user='me')
            raw_tracks = current.playlist_tracks
            playlist_tracks = []
            for track in raw_tracks:
                playlist_tracks.append(track.to_dict())
            is_empty = len(playlist_tracks) == 0
        except:
            playlist_tracks = []
            is_empty = True

        if is_empty:
            last_result = None
            for file in files:
                if isinstance(file, (str, Path)):
                    with open(file, 'rb') as f:
                        file_bytes = f.read()
                else:
                    file_bytes = file

                audio_info = media.Audio.get_audio_info(file_bytes)
                upload = await self.upload_file(file)

                last_result = await self.request(
                    method = 'addSavedMusicTrack',
                    input = {
                        'object_guid': self.guid,
                        'added_track': {
                            "file_id": upload.file_id,
                            "dc_id": upload.dc_id,
                            "access_hash_rec": upload.access_hash_rec,
                            "mime": upload.mime,
                            "file_name": upload.file_name,
                            "size": upload.size,
                            "type": "Music",
                            "time": audio_info.duration,
                            "music_performer": audio_info.performer or "<unknown>",
                            "width": 0,
                            "height": 0,
                            "is_spoil": False,
                            "is_round": False
                        }
                    }
                )
            return last_result

        for file in files:
            if isinstance(file, (str, Path)):
                with open(file, 'rb') as f:
                    file_bytes = f.read()
            else:
                file_bytes = file

            audio_info = media.Audio.get_audio_info(file_bytes)
            upload = await self.upload_file(file)

            playlist_tracks.append({
                "file_id": upload.file_id,
                "dc_id": upload.dc_id,
                "access_hash_rec": upload.access_hash_rec,
                "mime": upload.mime,
                "file_name": upload.file_name,
                "size": upload.size,
                "type": "Music",
                "time": audio_info.duration,
                "music_performer": audio_info.performer or "<unknown>",
                "width": 0,
                "height": 0,
                "is_spoil": False,
                "is_round": False
            })

        return await self.request(
            method = 'setSavedMusicPlaylist',
            input = {
                'object_guid': self.guid,
                'playlist_tracks': playlist_tracks
            }
        )