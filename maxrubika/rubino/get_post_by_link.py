from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPostByLink:
    async def get_post_by_link(
        self: "maxrubika.Rubino",
        link: str,
        my_profile: Optional[str] = None
    ):
        """
        Get a post by its link.

        Parameters:
            link (str): The link of the post.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The post data.
        """
        share_string = link.split('/')[-1]

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'share_string': share_string
        }

        return await self.request(
            method='getPostByShareLink',
            input=input_data
        )