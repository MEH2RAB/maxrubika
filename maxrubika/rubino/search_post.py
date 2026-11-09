from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SearchPost:
    async def search_post(
        self: "maxrubika.Rubino",
        search_text: Optional[str] = None,
        search_key: Optional[str] = None,
        usage: Literal['Search', 'Hashtag', 'Reels', 'Location'] = 'Search',
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Search for posts.

        Parameters:
            search_text (str, optional): The search text. Required for 'Search', 'Hashtag', and 'Reels'. Defaults to None.
            search_key (str, optional): The location ID. Required for 'Location'. Defaults to None.
            usage (Literal['Search', 'Hashtag', 'Reels', 'Location']): The search usage context. Case-insensitive. Default is 'Search'.
            start_id (str, optional): The starting post ID for pagination. Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        usage_map = {
            'search': 'Search',
            'hashtag': 'Hashtag',
            'reels': 'Reels',
            'location': 'Location'
        }

        normalized_usage = usage_map.get(usage.lower()) if isinstance(usage, str) else None
        if not normalized_usage:
            message = "'usage' must be 'Search', 'Hashtag', 'Reels', or 'Location'."
            raise InvalidInput(message)

        if normalized_usage in ('Search', 'Hashtag', 'Reels') and not search_text:
            message = f"'search_text' is required for usage '{normalized_usage}'."
            raise InvalidInput(message)

        if normalized_usage == 'Location' and not search_key:
            message = "'search_key' (location ID) is required for usage 'Location'."
            raise InvalidInput(message)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'usage': normalized_usage
        }

        if search_text is not None:
            input_data['search_text'] = search_text.replace('#', '')

        if search_key is not None:
            input_data['search_key'] = search_key

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='searchPost',
            input=input_data
        )