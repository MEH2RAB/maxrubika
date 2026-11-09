from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeletePageAvatar:
    async def delete_page_avatar(
        self: "maxrubika.Rubino",
        my_profile: Optional[str] = None
    ):
        """
        Delete the avatar of a page (profile).

        Parameters:
            my_profile (str, optional): The profile whose avatar is deleted. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'avatar_file': None,
            'updated_parameters': ['avatar_file']
        }

        return await self.request(
            method='updateProfile',
            input=input_data
        )