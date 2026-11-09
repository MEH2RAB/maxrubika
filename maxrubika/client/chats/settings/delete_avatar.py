from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteAvatar:
    async def delete_avatar(
        self: "maxrubika.Messenger",
        chat: str,
        avatar_id: str
    ):
        """
        Delete an avatar.

        Parameters:
            chat (str): The GUID, link, or username of the chat that owns the avatar.
            avatar_id (str): The identifier of the avatar to be deleted.

        Returns:
            The result of the API call.

        Note:
            If `chat` is 'me', 'cloud', 'self', or 'myself', it will be replaced with the client's GUID.
        """
        from ...exceptions import InvalidInput

        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")) and chat_guid != self.guid:
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        input_data = {'object_guid': chat_guid, 'avatar_id': avatar_id}

        return await self.request(method='deleteAvatar', input=input_data)