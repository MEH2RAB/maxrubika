from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetProfilePosts:
    async def get_profile_posts(
        self: "maxrubika.Rubino",
        target_profile: str,
        post_type: Literal['IGTV', 'Reels', 'Tagged', 'All'] = 'All',
        limit: Optional[int] = None,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get the posts of a profile.

        Parameters:
            target_profile (str): The profile ID or username to query.
            post_type (Literal['IGTV', 'Reels', 'Tagged', 'All']): The post type filter. Case-insensitive. Default is 'All'.
            limit (int, optional): The maximum number of posts to return. Defaults to None (server default).
            start_id (str, optional): The starting post ID for pagination. Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        type_map = {
            'igtv': 'IGTV',
            'reels': 'Reels',
            'tagged': 'Tagged',
            'all': 'All'
        }

        normalized_type = type_map.get(post_type.lower()) if isinstance(post_type, str) else None
        if not normalized_type:
            message = "'post_type' must be 'IGTV', 'Reels', 'Tagged', or 'All'."
            raise InvalidInput(message)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        target_profile_id = await self.get_profile_id(target_profile)

        input_data = {
            'profile_id': profile_id,
            'target_profile_id': target_profile_id,
            'post_type': normalized_type
        }

        if limit is not None:
            input_data['limit'] = limit

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getProfilePosts',
            input=input_data
        )