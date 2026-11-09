from typing import Optional, Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetProfileAdmin:
    async def set_profile_admin(
        self: "maxrubika.Rubino",
        target_profile: str,
        access: Union[str, List[str]],
        my_profile: Optional[str] = None
    ):
        """
        Set admin access for a profile.

        Parameters:
            target_profile (str): The profile ID or username of the admin.
            access (Union[str, List[str]]): A single access permission or a list of them. Pass 'All' (case-insensitive) to grant all permissions.
            my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        access_list_options = [
            'ManagePost',
            'ManageStory',
            'ManageComment',
            'UpdateProfile',
            'ChangeProfileType',
            'AddAdmin',
            'ManageLive',
            'SocialActivityOnPost',
            'SocialActivityOnProfile',
            'ManageSetting'
        ]

        if isinstance(access, str):
            access = [access]

        if not isinstance(access, list) or not access:
            message = "'access' must be a non-empty string or list."
            raise InvalidInput(message)

        access_map = {item.lower(): item for item in access_list_options}
        normalized_access = []

        for item in access:
            if not isinstance(item, str):
                message = f"Invalid access item: {item!r}."
                raise InvalidInput(message)

            key = item.lower()

            if key == 'all':
                normalized_access = list(access_list_options)
                break

            mapped = access_map.get(key)
            if not mapped:
                message = f"Invalid access item '{item}'. Allowed: {', '.join(access_list_options)} or 'All'."
                raise InvalidInput(message)

            if mapped not in normalized_access:
                normalized_access.append(mapped)

        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'target_profile_id': target_profile_id,
            'action': 'Set',
            'access_list': normalized_access
        }

        return await self.request(
            method='setProfileAdmin',
            input=input_data
        )