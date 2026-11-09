from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteContact:
    async def delete_contact(self: "maxrubika.Messenger", user: str):
        """
        Deletes a contact from the client's address book.

        Parameters:
            user (str): The GUID or username of the contact to be deleted.

        Returns:
            The result of the contact deletion operation.

        Note:
            The `user` parameter should be the GUID or username of the contact to be deleted.
        """
        from ..exceptions import InvalidInput

        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        return await self.request(method='deleteContact', input={'user_guid': user_guid})