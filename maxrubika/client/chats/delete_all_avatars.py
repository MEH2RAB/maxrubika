import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class DeleteAllAvatars:
    async def delete_all_avatars(self: "maxrubika.Client", chat: str):
        """
        Delete all avatars from a chat or user profile.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            Data: Result of the operation.

        Note:
            If `chat` is 'me', 'cloud', 'self', or 'myself', it will be replaced with the client's GUID.
        """
        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")) and chat_guid != self.guid:
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        response = await self.get_avatars(chat_guid)
        response_data = response.to_dict() if hasattr(response, 'to_dict') else response

        avatar_list = response_data.get('avatars', [])

        if not avatar_list:
            return Data({"status": "OK", "message": "No avatars to delete."})

        deleted_count = 0
        for avatar in avatar_list:
            avatar_id = avatar.get('avatar_id') if isinstance(avatar, dict) else getattr(avatar, 'avatar_id', None)
            if avatar_id:
                await self.delete_avatar(chat_guid, avatar_id)
                deleted_count += 1

        return Data({
            "status": "OK",
            "message": "All avatars deleted successfully.",
            "deleted_count": deleted_count
        })