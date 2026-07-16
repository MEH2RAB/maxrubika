import maxrubika
from ..exceptions import InvalidInput

class GetSavedMusicPlaylist:
    async def get_saved_music_playlist(self: "maxrubika.Client", user: str):
        """
        Get the saved music playlist of a user.

        Parameters:
            user (str): The GUID or username of the user.

        Returns:
            The result of the API call containing saved music playlist.
        """
        if user.lower() in ('me', 'cloud', 'self', 'myself'):
            user_guid = self.guid
        else:
            user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        return await self.request(
            method = 'getSavedMusicPlaylist',
            input = {'object_guid': user_guid}
        )