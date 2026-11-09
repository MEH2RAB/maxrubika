from typing import Union, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnsetCloseFriends:
    async def unset_close_friends(
        self: "maxrubika.Rubino",
        target_profiles: Union[str, List[str]],
        my_profile: Optional[str] = None
    ):
        """
        Remove profiles from close friends.

        Parameters:
            target_profiles (Union[str, List[str]]): A profile ID/username or a list of profile IDs/usernames to remove from close friends.
            my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

        Returns:
            The response data.

        Examples:
            # Remove a single close friend
            await client.unset_close_friends(
                target_profiles="u0abc123def",
                my_profile="MAXRubikaTest"
            )

            # Remove multiple close friends
            await client.unset_close_friends(
                target_profiles=["u0abc123def", "u0xyz789ghi"],
                my_profile="MAXRubikaTest"
            )
        """
        from .exceptions import InvalidInput

        if isinstance(target_profiles, str):
            target_profiles = [target_profiles]

        if not isinstance(target_profiles, list) or not target_profiles:
            raise InvalidInput("'target_profiles' must be a non-empty string or list.")

        target_profile_ids = []
        for profile in target_profiles:
            profile_id = await self.get_profile_id(profile)
            if profile_id not in target_profile_ids:
                target_profile_ids.append(profile_id)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'target_profile_ids': target_profile_ids,
            'action_type': 'Unset'
        }

        return await self.request(
            method='closeFriendAction',
            input=input_data
        )