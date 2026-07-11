import maxrubika
from ..exceptions import InvalidInput

class ChangeOwner:
    async def change_owner(
        self: "maxrubika.Client",
        chat: str,
        new_owner: str
    ):
        """
        Request to transfer ownership of a chat to another user.

        Parameters:
            chat (str): The GUID, link, or username of the chat (channel/group).
            new_owner (str): The GUID or username of the user to become new owner.

        Returns:
            The result of the API call.

        Note:
            - Only works if you are the current owner
            - New owner must accept the request
            - Irreversible action
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        user_guid = await self.get_guid(new_owner)

        if not user_guid.startswith("u0"):
            message = f"'{new_owner}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        return await self.request(
            method = 'requestChangeObjectOwner',
            input = {
                'object_guid': chat_guid,
                'new_owner_user_guid': user_guid
            }
        )
