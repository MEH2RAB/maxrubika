import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class StartVoiceChat:
    async def start_voice_chat(
        self: "maxrubika.Messenger",
        chat: str,
        version: int = 1
    ):
        """
        Start a voice chat for a channel or group.

        Parameters:
            chat (str): The GUID, link, or username of the channel/group.
            version (int): Voice chat protocol version. Default: 1.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        input_data = {
            'chat_guid': chat_guid,
            'version': version,
            'rnd': random.randint(100000, 999999)
        }

        return await self.request(
            method='createGroupVoiceChat',
            input=input_data
        )