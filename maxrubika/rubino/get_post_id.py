import re
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPostID:
    async def get_post_id(
        self: "maxrubika.Rubino",
        post: str,
        my_profile: Optional[str] = None
    ) -> str:
        """
        Get post ID from a share link or post ID.

        Parameters:
            post (str): The share link or post ID.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The post ID string.
        """
        from .exceptions import InvalidPostLink, PostNotAccessible
        from ..data import Data

        if re.match(r'^[0-9a-f]{24}$', post):
            return post

        result = await self.get_post_by_link(post, my_profile=my_profile)

        if isinstance(result, dict):
            result = Data(result)

        post_data = result.find_keys('post')

        if not post_data:
            status = result.find_keys('status')
            has_access = result.find_keys('has_access')
            if status == 'NoAccess' or has_access is False:
                raise PostNotAccessible()
            raise InvalidPostLink()

        if isinstance(post_data, dict):
            post_data = Data(post_data)

        return post_data.find_keys('id')