from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RemoveFollower:
    async def remove_follower(
        self: "maxrubika.Rubino",
        target_profile: str,
        post_track_id: Optional[str] = None,
        profile_track_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Remove a follower from a profile.

        Parameters:
            target_profile (str): The profile ID or username of the follower to remove.
            post_track_id (str, optional): The post track ID. Defaults to None.
            profile_track_id (str, optional): The profile track ID. Defaults to None.
            my_profile (str, optional): The profile that removes the follower. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'target_profile_id': target_profile_id,
            'action': 'RemoveFollower'
        }

        action_data = {}
        if post_track_id is not None:
            action_data['post_track_id'] = post_track_id
        if profile_track_id is not None:
            action_data['profile_track_id'] = profile_track_id

        if action_data:
            input_data['action_data'] = action_data

        return await self.request(
            method='profileAction',
            input=input_data
        )