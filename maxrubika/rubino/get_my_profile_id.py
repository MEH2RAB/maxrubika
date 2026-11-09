from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMyProfileID:
    async def get_my_profile_id(self: "maxrubika.Rubino") -> str:
        """
        Get the current user's profile ID.

        Returns:
            str: The user's profile ID.
        """
        return self.profile_id