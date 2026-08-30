import maxrubika
from ..exceptions import InvalidInput

class DeleteUserChat:
    async def delete_user_chat(
        self: "maxrubika.Client",
        user: str
    ):
        """
        Delete a user chat.

        Parameters:
            user (str): The GUID or username of the user whose chat is to be deleted.

        Returns:
            The result of the user chat deletion.
        """
        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        last_message = await self.get_last_message(user_guid)
        last_data = last_message.to_dict() if hasattr(last_message, 'to_dict') else last_message

        message = last_data.get('message')

        if isinstance(message, dict):
            last_deleted_message_id = message.get('message_id', 0)
        else:
            last_deleted_message_id = 0

        return await self.request(
            method = 'deleteUserChat',
            input = {
                'user_guid': user_guid,
                'last_deleted_message_id': last_deleted_message_id
            }
        )