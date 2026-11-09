from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RejectFollowRequest:
    async def reject_follow_request(
        self: "maxrubika.Rubino",
        target_profile: str,
        post_track_id: Optional[str] = None,
        profile_track_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Reject a follow request.

        Parameters:
            target_profile (str): The profile ID or username that sent the follow request.
            post_track_id (str, optional): The post track ID. Only used in API version 1.
            profile_track_id (str, optional): The profile track ID. Only used in API version 1.
            my_profile (str, optional): The profile that rejects. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        if self.api_version == 1:
            input_data = {
                'profile_id': profile_id,
                'target_profile_id': target_profile_id,
                'action': 'DeclineFollowRequest'
            }

            action_data = {}
            if post_track_id is not None:
                action_data['post_track_id'] = post_track_id
            if profile_track_id is not None:
                action_data['profile_track_id'] = profile_track_id

            if action_data:
                input_data['action_data'] = action_data

            method = 'profileAction'
        else:
            input_data = {
                'profile_id': profile_id,
                'action': 'Decline',
                'request_id': target_profile_id
            }
            method = 'actionOnRequest'

        return await self.request(
            method=method,
            input=input_data
        )