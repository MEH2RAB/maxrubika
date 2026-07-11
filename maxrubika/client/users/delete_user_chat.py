from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class DeleteUserChat:
    async def delete_user_chat(
        self: "maxrubika.Client",
        user: str,
        last_deleted_message_id: Union[str, int]
    ):
        """
        Delete a user chat.

        Parameters:
            user (str): The GUID or username of the user whose chat is to be deleted.
            last_deleted_message_id (Union[str, int]): The last deleted message ID.

        Returns:
            The result of the user chat deletion.
        """
        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        return await self.request(
            method = 'deleteUserChat',
            input = {
                'user_guid': user_guid,
                'last_deleted_message_id': last_deleted_message_id
            }
        )