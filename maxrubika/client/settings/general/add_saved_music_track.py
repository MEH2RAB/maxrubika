from typing import Union, Optional, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    import maxrubika

class AddSavedMusicTrack:
    async def add_saved_music_track(
        self: "maxrubika.Messenger",
        track: Optional[Union[Path, str, bytes]] = None,
        file_inline: Optional[dict] = None,
        time: Optional[int] = None,
        performer: Optional[str] = None,
        file_name: Optional[str] = None,
        **kwargs
    ):
        """
        Add a single music track to your saved music playlist.

        Parameters:
            track (Union[Path, str, bytes], optional): A file path or raw bytes.
            file_inline (dict, optional): A pre-uploaded file_inline dict to add directly.
            time (int, optional): Custom duration in seconds. Auto-detected if not provided.
            performer (str, optional): Custom performer name. Auto-detected if not provided.
            file_name (str, optional): Custom file name. Uses original file name if not provided.

        Returns:
            The result of the API call.
        """
        import aiofiles
        from ...core import media
        from ...exceptions import InvalidInput

        if file_inline is not None:
            if file_name:
                file_inline = {**file_inline, "file_name": file_name}

            input_data = {
                'object_guid': self.guid,
                'added_track': file_inline
            }

            return await self.request(method='addSavedMusicTrack', input=input_data)

        if track is None:
            raise InvalidInput("Either 'track' or 'file_inline' must be provided.")

        if isinstance(track, (str, Path)):
            async with aiofiles.open(track, 'rb') as f:
                file_bytes = await f.read()
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

        input_data = {
            'object_guid': self.guid,
            'added_track': added_track
        }

        return await self.request(method='addSavedMusicTrack', input=input_data)