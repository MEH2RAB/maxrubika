from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPostComments:
    async def get_post_comments(
        self: "maxrubika.Rubino",
        target_profile: str,
        post: str,
        type: Literal['Main', 'Reply'] = 'Main',
        parent_id: Optional[str] = None,
        start_id: Optional[str] = None,
        comment_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get comments of a post.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post (str): The post link or post ID.
            type (Literal['Main', 'Reply']): The comment type. Case-insensitive. Default is 'Main'.
            parent_id (str, optional): The parent comment ID (used with 'Reply'). Defaults to None.
            start_id (str, optional): The starting comment ID for pagination. Defaults to None.
            comment_id (str, optional): A specific comment ID (used with 'Reply'). Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        type_map = {
            'main': 'Main',
            'reply': 'Reply'
        }
        type = type_map.get(type.lower()) if isinstance(type, str) else None

        if not type:
            message = "'type' must be 'Main' or 'Reply'."
            raise InvalidInput(message)

        post_id = await self.get_post_id(post, my_profile=my_profile)
        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'post_profile_id': target_profile_id,
            'post_id': post_id,
            'type': type
        }

        if parent_id is not None:
            input_data['parent_id'] = parent_id

        if start_id is not None:
            input_data['start_id'] = start_id

        if comment_id is not None:
            input_data['comment_id'] = comment_id

        return await self.request(
            method='getPostComments',
            input=input_data
        )