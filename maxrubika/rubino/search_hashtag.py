from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SearchHashtag:
    async def search_hashtag(
        self: "maxrubika.Rubino",
        search_text: str,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Search for hashtags.

        Parameters:
            search_text (str): The search text (hashtag name without '#').
            start_id (str, optional): The starting hashtag ID for pagination. Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        normalized = search_text.replace('#', '').strip()

        if not normalized:
            message = "'search_text' must be a non-empty string."
            raise InvalidInput(message)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'search_text': normalized
        }

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='searchHashTag',
            input=input_data
        )