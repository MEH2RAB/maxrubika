from random import randint
from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AddPostComment:
    async def add_post_comment(
        self: "maxrubika.Rubino",
        target_profile: str,
        post: str,
        text: str,
        type: Literal['Main', 'Reply'] = 'Main',
        parent_id: Optional[str] = None,
        post_track_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Add a comment to a post.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post (str): The post link or post ID.
            text (str): The comment text.
            type (Literal['Main', 'Reply']): The comment type. Case-insensitive. Default is 'Main'.
            parent_id (str, optional): The parent comment ID (used with 'Reply'). Defaults to None.
            post_track_id (str, optional): The post track ID. Defaults to None.
            my_profile (str, optional): The profile that comments. Defaults to self.profile_id.

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

        rnd = randint(100000, 999999999)

        if self.api_version == 1:
            input_data = {
                'profile_id': profile_id,
                'post_id': post_id,
                'post_profile_id': target_profile_id,
                'content': text,
                'type': type,
                'rnd': rnd
            }

            if parent_id is not None:
                input_data['parent_id'] = parent_id

            if post_track_id is not None:
                input_data['post_track_id'] = post_track_id

            method = 'addPostComment'
        else:
            input_data = {
                'profile_id': profile_id,
                'post_id': post_id,
                'post_profile_id': target_profile_id,
                'content': text,
                'rnd': rnd
            }
            method = 'addComment'

        return await self.request(
            method=method,
            input=input_data
        )