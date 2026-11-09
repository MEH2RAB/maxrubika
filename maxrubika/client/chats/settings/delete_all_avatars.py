from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteAllAvatars:
    async def delete_all_avatars(
        self: "maxrubika.Messenger",
        chat: str
    ):
        """
        Delete all avatars from a chat or user profile.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            Data or dict: Result of the operation.

        Note:
            If `chat` is 'me', 'cloud', 'self', or 'myself', it will be replaced with the client's GUID.
        """
        from ....data import Data
        from ...exceptions import InvalidInput

        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")) and chat_guid != self.guid:
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        response = await self.get_avatars(chat_guid)

        if isinstance(response, dict):
            response = Data(response)

        avatar_list = response.find_keys('avatars') or []

        if not avatar_list:
            result_dict = {
                "status": "OK",
                "message": "No avatars to delete.",
                "deleted_count": 0
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        deleted_count = 0
        for avatar in avatar_list:
            if isinstance(avatar, dict):
                avatar = Data(avatar)

            avatar_id = avatar.find_keys('avatar_id')
            if avatar_id:
                await self.delete_avatar(chat_guid, avatar_id)
                deleted_count += 1

        result_dict = {
            "status": "OK",
            "message": "All avatars deleted successfully.",
            "deleted_count": deleted_count
        }
        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)