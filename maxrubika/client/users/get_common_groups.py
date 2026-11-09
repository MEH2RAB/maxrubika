from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetCommonGroups:
    async def get_common_groups(self: "maxrubika.Messenger", user: str):
        """
        Get groups in common with a user.

        Parameters:
            user (str): User's GUID/username.

        Returns:
            Common groups list.
        """
        from ..exceptions import InvalidInput

        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        return await self.request(
            method='getCommonGroups',
            input={'user_guid': user_guid}
        )