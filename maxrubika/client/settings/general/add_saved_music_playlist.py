from typing import Union, List, Optional, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    import maxrubika

class AddSavedMusicPlaylist:
    async def add_saved_music_playlist(
        self: "maxrubika.Messenger",
        files: Optional[Union[Path, str, List[Union[Path, str]]]] = None,
        file_inlines: Optional[List[dict]] = None,
        time: Optional[int] = None,
        performer: Optional[str] = None,
        file_name: Optional[str] = None,
        **kwargs
    ):
        """
        Add a saved music playlist on your profile.

        Parameters:
            files (Union[Path, str, List], optional): A single file path or a list of file paths.
            file_inlines (List[dict], optional): Pre-uploaded file_inline dicts to add directly.
            time (int, optional): Custom duration in seconds. Auto-detected if not provided.
            performer (str, optional): Custom performer name. Auto-detected if not provided.
            file_name (str, optional): Custom file name. Uses original file name if not provided.

        Returns:
            The result of the API call.
        """
        import aiofiles
        from ...core import media

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
                    async with aiofiles.open(file, 'rb') as f:
                        file_bytes = await f.read()
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
            input_data = {
                'object_guid': self.guid,
                'added_track': track
            }
            last_result = await self.request(method='addSavedMusicTrack', input=input_data)
        return last_result