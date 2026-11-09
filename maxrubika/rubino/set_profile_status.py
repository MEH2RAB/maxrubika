from typing import Literal, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetProfileStatus:
    async def set_profile_status(
        self: "maxrubika.Rubino",
        profile_status: Literal['Public', 'Private'],
        my_profile: Optional[str] = None
    ):
        """
        Set the visibility status of a page (profile).

        Parameters:
            profile_status (Literal['Public', 'Private']): The new visibility. Case-insensitive.
            my_profile (str, optional): The profile to update. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        return await self.update_page(
            profile_status=profile_status,
            my_profile=my_profile
        )