import maxrubika
from ..exceptions import InvalidInput

class StartVoiceChat:
    async def start_voice_chat(self: "maxrubika.Client", chat: str):
        """
        Start a voice chat for a channel or group.

        Parameters:
            chat (str): The GUID, link, or username of the channel/group.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        return await self.request(
            method = 'createGroupVoiceChat',
            input = {'chat_guid': chat_guid}
        )