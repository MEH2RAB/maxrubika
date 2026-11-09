from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeletePage:
    async def delete_page(
        self: "maxrubika.Rubino",
        target_profile: str,
        my_profile: Optional[str] = None
    ):
        """
        Delete a page (profile).

        Parameters:
            target_profile (str): The profile ID or username of the page to delete.
            my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        target_profile_id = await self.get_profile_id(target_profile)

        if self.api_version == 1:
            if my_profile is None:
                profile_id = self.profile_id
            else:
                profile_id = await self.get_profile_id(my_profile)

            input_data = {
                'profile_id': profile_id,
                'target_profile_id': target_profile_id
            }
            method = 'removeProfile'
        else:
            input_data = {
                'model': 'Profile',
                'record_id': target_profile_id
            }
            method = 'removeRecord'

        return await self.request(
            method=method,
            input=input_data
        )