from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPostsByHashtag:
    async def get_posts_by_hashtag(
        self: "maxrubika.Rubino",
        hashtag: str,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get posts by hashtag.

        Parameters:
            hashtag (str): The hashtag name.
            start_id (str, optional): The starting post ID for pagination. Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        return await self.search_post(
            search_text=hashtag.replace('#', '').strip(),
            usage='Hashtag',
            start_id=start_id,
            my_profile=my_profile
        )