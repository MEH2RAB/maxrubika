from typing import Literal, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetProfileType:
    async def set_profile_type(
        self: "maxrubika.Rubino",
        profile_type: Literal['Business', 'Personal', 'Creator'],
        my_profile: Optional[str] = None
    ):
        """
        Set the type of a page (profile).

        Parameters:
            profile_type (Literal['Business', 'Personal', 'Creator']): The new page type. Case-insensitive.
            my_profile (str, optional): The profile to update. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        return await self.update_page(
            profile_type=profile_type,
            my_profile=my_profile
        )