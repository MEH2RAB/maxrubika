import maxrubika
from ..exceptions import InvalidInput

class GetCommonGroups:
    async def get_common_groups(self: "maxrubika.Client", user: str):
        """
        Get groups in common with a user.

        Parameters:
            user (str): User's GUID/username.

        Returns:
            Common groups list.
        """
        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        return await self.request(
            method = 'getCommonGroups',
            input = {'user_guid': user_guid}
        )