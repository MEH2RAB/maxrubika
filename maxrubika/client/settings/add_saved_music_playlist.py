from typing import Union, List, Optional
from pathlib import Path
import maxrubika
from ..core import media

class AddSavedMusicPlaylist:
    async def add_saved_music_playlist(
        self: "maxrubika.Client",
        files: Union[Path, str, List[Union[Path, str]]] = None,
        file_inlines: List[dict] = None,
        time: Optional[int] = None,
        performer: Optional[str] = None,
        file_name: Optional[str] = None,
        **kwargs
    ):
        """
        Add a saved music playlist on your profile.

        Parameters:
            files: A single file path or a list of file paths to music files.
            file_inlines: Pre-uploaded file_inline dicts to add directly.
            time: Custom duration in seconds. If not provided, auto-detected.
            performer: Custom performer name. If not provided, auto-detected.
            file_name: Custom file name. If not provided, uses original file name.

        Returns:
            The result of the API call.
        """
        tracks = []

        if file_inlines:
            if isinstance(file_inlines, dict):
                file_inlines = [file_inlines]
            for fi in file_inlines:
                if file_name:
                    fi = {**fi, "file_name": file_name}
                tracks.append(fi)

        if files:
            if isinstance(files, (str, Path)):
                files = [files]

            for file in files:
                if isinstance(file, (str, Path)):
                    with open(file, 'rb') as f:
                        file_bytes = f.read()
                else:
                    file_bytes = file

                audio_info = None
                if time is None or performer is None:
                    audio_info = media.Audio.get_audio_info(file_bytes)

                upload = await self.upload_file(file, **kwargs)

                tracks.append({
                    "file_id": upload.file_id,
                    "dc_id": upload.dc_id,
                    "access_hash_rec": upload.access_hash_rec,
                    "mime": upload.mime,
                    "file_name": file_name if file_name else upload.file_name,
                    "size": upload.size,
                    "type": "Music",
                    "time": time if time is not None else (audio_info.duration if audio_info else 1),
                    "music_performer": performer if performer is not None else (audio_info.performer if audio_info else "<unknown>"),
                    "width": 0,
                    "height": 0,
                    "is_spoil": False,
                    "is_round": False
                })

        last_result = None
        for track in tracks:
            last_result = await self.request(
                method='addSavedMusicTrack',
                input={
                    'object_guid': self.guid,
                    'added_track': track
                }
            )
        return last_result