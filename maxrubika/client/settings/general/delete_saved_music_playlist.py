from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteSavedMusicPlaylist:
    async def delete_saved_music_playlist(
        self: "maxrubika.Messenger",
        position: Optional[int] = None
    ):
        """
        Delete tracks from the saved music playlist on your profile.

        Parameters:
            position (int, optional): The position of the track to delete. If None, deletes all.

        Returns:
            The result of the API call.
        """
        if position is None:
            input_data = {
                'object_guid': self.guid,
                'playlist_tracks': []
            }

            return await self.request(method='setSavedMusicPlaylist', input=input_data)

        try:
            current = await self.get_saved_music_playlist(user='me')
            raw_tracks = current.playlist_tracks
            playlist_tracks = []

            for i, track in enumerate(raw_tracks):
                track_dict = track.to_dict() if hasattr(track, 'to_dict') else track

                if i != position - 1:
                    playlist_tracks.append(track_dict)

        except Exception:
            return None

        input_data = {
            'object_guid': self.guid,
            'playlist_tracks': playlist_tracks
        }

        return await self.request(method='setSavedMusicPlaylist', input=input_data)