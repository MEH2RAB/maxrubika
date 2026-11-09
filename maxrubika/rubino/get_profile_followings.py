from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetProfileFollowings:
    async def get_profile_followings(
        self: "maxrubika.Rubino",
        target_profile: str,
        search_text: Optional[str] = None,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get the following list of a profile.

        Parameters:
            target_profile (str): The profile ID or username to query.
            search_text (str, optional): Search text for filtering. Defaults to None.
            start_id (str, optional): The starting user ID for pagination. Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        target_profile_id = await self.get_profile_id(target_profile)

        input_data = {
            'profile_id': profile_id,
            'target_profile_id': target_profile_id,
            'type': 'Following'
        }

        if search_text is not None:
            input_data['search_text'] = search_text

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getProfileFollowers',
            input=input_data
        )