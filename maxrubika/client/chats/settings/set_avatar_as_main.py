from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetAvatarAsMain:
    async def set_avatar_as_main(
        self: "maxrubika.Messenger",
        chat: str,
        avatar_id: str
    ):
        """
        Set an avatar as the main avatar for a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat, or 'me'/'cloud'/'self'/'myself'.
            avatar_id (str): The ID of the avatar to set as main.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")) and chat_guid != self.guid:
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        input_data = {
            'object_guid': chat_guid,
            'avatar_id': avatar_id
        }

        return await self.request(
            method='updateAvatar',
            input=input_data
        )