from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetProfileAdmins:
    async def get_profile_admins(
        self: "maxrubika.Rubino",
        my_profile: Optional[str] = None
    ):
        """
        Get the list of admins of a profile (page).

        Parameters:
            my_profile (str, optional): The profile to query. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        return await self.request(
            method='getProfileAdmins',
            input={'profile_id': profile_id}
        )