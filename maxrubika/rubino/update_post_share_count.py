from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UpdatePostShareCount:
    async def update_post_share_count(
        self: "maxrubika.Rubino",
        target_profile: str,
        post: str,
        target_object_type: Literal['User', 'Channel', 'Group', 'Service', 'Bot'] = 'Channel',
        target_object_id: Optional[str] = None,
        type: str = 'Message',
        track_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Update the share count of a post.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post (str): The post link or post ID.
            target_object_type (Literal['User', 'Channel', 'Group', 'Service', 'Bot']): The type of the destination object. Case-insensitive.
            target_object_id (str, optional): The ID of the destination (chat/channel/group). Defaults to None.
            type (str, optional): The share type. Default is 'Message'.
            track_id (str, optional): A tracking ID. Defaults to None.
            my_profile (str, optional): The profile that shares. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        type_map = {
            'user': 'User',
            'channel': 'Channel',
            'group': 'Group',
            'service': 'Service',
            'bot': 'Bot'
        }

        normalized_type = type_map.get(target_object_type.lower()) if isinstance(target_object_type, str) else None
        if not normalized_type:
            message = "'target_object_type' must be 'User', 'Channel', 'Group', 'Service', or 'Bot'."
            raise InvalidInput(message)

        post_id = await self.get_post_id(post, my_profile=my_profile)
        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'post_id': post_id,
            'post_profile_id': target_profile_id,
            'type': type,
            'target_object_type': normalized_type
        }

        if target_object_id is not None:
            input_data['target_object_id'] = target_object_id

        if track_id is not None:
            input_data['track_id'] = track_id

        return await self.request(
            method='updatePostShareCount',
            input=input_data
        )