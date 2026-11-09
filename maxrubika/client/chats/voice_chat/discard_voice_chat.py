from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DiscardVoiceChat:
    async def discard_voice_chat(
        self: "maxrubika.Messenger",
        chat: str,
        voice_chat_id: Optional[str] = None
    ):
        """
        Discard/end a voice chat for a channel or group.

        Parameters:
            chat (str): The GUID, link, or username of the channel or group.
            voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

        Returns:
            The result of the API call.
        """
        from ....data import Data
        from ...exceptions import InvalidInput, VoiceChatNotActive

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        if not voice_chat_id:
            chat_info = await self.get_chat_info(chat_guid)
            data = Data(chat_info)
            voice_chat_id = data.find_keys("group_voice_chat_id")

            if not voice_chat_id:
                raise VoiceChatNotActive()

        input_data = {
            'chat_guid': chat_guid,
            'voice_chat_id': voice_chat_id
        }

        return await self.request(
            method='discardGroupVoiceChat',
            input=input_data
        )