from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UnblockUser:
    async def unblock_user(self: "maxrubika.Messenger", user: str):
        """
        Unblock a user.

        Parameters:
            user (str): The GUID or username of the user to unblock.

        Returns:
            The result of the unblock operation.
        """
        from ..exceptions import InvalidInput

        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        input_data = {'user_guid': user_guid, 'action': 'Unblock'}
        return await self.request(
            method='setBlockUser',
            input=input_data
        )