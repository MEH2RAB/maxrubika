from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetPostFeedback:
    async def set_post_feedback(
        self: "maxrubika.Rubino",
        target_profile: str,
        post: str,
        action: Literal['Interested', 'NotInterested'] = 'Interested',
        track_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Set feedback (interested/not interested) for a post.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post (str): The post link or post ID.
            action (Literal['Interested', 'NotInterested']): The feedback action. Case-insensitive. Default is 'Interested'.
            track_id (str, optional): A tracking ID. Defaults to None.
            my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        action_map = {
            'interested': 'Interested',
            'notinterested': 'NotInterested'
        }

        normalized_action = action_map.get(action.lower()) if isinstance(action, str) else None
        if not normalized_action:
            message = "'action' must be 'Interested' or 'NotInterested'."
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
            'action': normalized_action
        }

        if track_id is not None:
            input_data['track_id'] = track_id

        return await self.request(
            method='setPostFeedback',
            input=input_data
        )