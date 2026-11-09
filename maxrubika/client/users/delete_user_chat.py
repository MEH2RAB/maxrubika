from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteUserChat:
    async def delete_user_chat(
        self: "maxrubika.Messenger",
        user: str
    ):
        """
        Delete a user chat.

        Parameters:
            user (str): The GUID or username of the user whose chat is to be deleted.

        Returns:
            The result of the user chat deletion.
        """
        from ...data import Data
        from ..exceptions import InvalidInput

        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        last_message = await self.get_last_message(user_guid)

        if isinstance(last_message, dict):
            last_message = Data(last_message)

        last_deleted_message_id = last_message.find_keys('message_id') or 0

        input_data = {
            'user_guid': user_guid,
            'last_deleted_message_id': last_deleted_message_id
        }

        return await self.request(
            method='deleteUserChat',
            input=input_data
        )