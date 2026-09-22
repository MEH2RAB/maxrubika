from typing import Union, Optional
from pathlib import Path
import maxrubika
from ..core import media

class AddSavedMusicTrack:
    async def add_saved_music_track(
        self: "maxrubika.Client",
        track: Union[Path, str] = None,
        file_inline: dict = None,
        time: Optional[int] = None,
        performer: Optional[str] = None,
        file_name: Optional[str] = None,
        **kwargs
    ):
        """
        Add a single music track to your saved music playlist.

        Parameters:
            track: A file path (str or Path) to a music file, or raw bytes.
            file_inline: A pre-uploaded file_inline dict to add directly.
            time: Custom duration in seconds. If not provided, auto-detected.
            performer: Custom performer name. If not provided, auto-detected.
            file_name: Custom file name. If not provided, uses original file name.

        Returns:
            The result of the API call.
        """
        if file_inline is not None:
            if file_name:
                file_inline = {**file_inline, "file_name": file_name}

            return await self.request(
                method = 'addSavedMusicTrack',
                input = {
                    'object_guid': self.guid,
                    'added_track': file_inline
                }
            )

        if track is None:
            raise ValueError("Either 'track' or 'file_inline' must be provided.")

        if isinstance(track, (str, Path)):
            with open(track, 'rb') as f:
                file_bytes = f.read()
        else:
            file_bytes = track

        audio_info = None
        if time is None or performer is None:
            audio_info = media.Audio.get_audio_info(file_bytes)

        upload = await self.upload_file(track, **kwargs)

        added_track = {
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
        }

        return await self.request(
            method = 'addSavedMusicTrack',
            input = {
                'object_guid': self.guid,
                'added_track': added_track
            }
        )