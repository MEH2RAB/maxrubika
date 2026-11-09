from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetRelatedPosts:
    async def get_related_posts(
        self: "maxrubika.Rubino",
        location: Literal['Explore', 'SuggestedPost', 'ShowPost'],
        post_id: Optional[str] = None,
        target_profile: Optional[str] = None,
        track_id: Optional[str] = None,
        limit: Optional[int] = None,
        start_id: Optional[str] = None,
        post_position: Optional[dict] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get posts related to a given post.

        Parameters:
            location (Literal['Explore', 'SuggestedPost', 'ShowPost']): The context where related posts are shown. Case-insensitive.
            post_id (str, optional): The ID of the reference post. Defaults to None.
            target_profile (str, optional): The profile ID or username that owns the post. Defaults to None.
            track_id (str, optional): A tracking ID. Defaults to None.
            limit (int, optional): The maximum number of posts to return. Defaults to None (server default).
            start_id (str, optional): The starting post ID for pagination. Defaults to None.
            post_position (dict, optional): The position of the post in the grid, with 'row' (int) and 'column' (int). Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.

        Examples:
            # Explore related posts
            await client.get_related_posts(
                location="Explore",
                limit=10,
                my_profile="MAXRubikaTest"
            )

            # Suggested posts after viewing a post
            await client.get_related_posts(
                location="SuggestedPost",
                post_id="6ae61abdfc4eff521f9f0448",
                target_profile="Online_User",
                limit=10,
                my_profile="MAXRubikaTest"
            )

            # Related posts shown on a post page
            await client.get_related_posts(
                location="ShowPost",
                post_id="6ae61abdfc4eff521f9f0448",
                target_profile="Online_User",
                track_id='{"l": "SharePost"}',
                my_profile="MAXRubikaTest"
            )

            # With post position in the grid
            await client.get_related_posts(
                location="Explore",
                post_id="6ae61abdfc4eff521f9f0448",
                target_profile="Online_User",
                post_position={"row": 1, "column": 2},
                my_profile="MAXRubikaTest"
            )
        """
        from .exceptions import InvalidInput

        location_map = {
            'explore': 'Explore',
            'suggestedpost': 'SuggestedPost',
            'showpost': 'ShowPost'
        }

        normalized_location = location_map.get(location.lower()) if isinstance(location, str) else None
        if not normalized_location:
            message = "'location' must be 'Explore', 'SuggestedPost', or 'ShowPost'."
            raise InvalidInput(message)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'location': normalized_location
        }

        if post_id is not None:
            input_data['post_id'] = post_id

        if target_profile is not None:
            input_data['post_profile_id'] = await self.get_profile_id(target_profile)

        if track_id is not None:
            input_data['track_id'] = track_id

        if limit is not None:
            input_data['limit'] = limit

        if start_id is not None:
            input_data['start_id'] = start_id

        if post_position is not None:
            input_data['post_position'] = post_position

        return await self.request(
            method='getRelatedPosts',
            input=input_data
        )