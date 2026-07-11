import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class DiscardVoiceChat:
    async def discard_voice_chat(self: "maxrubika.Client", chat: str):
        """
        Discard/End a voice chat for a channel or group.

        Parameters:
            chat (str): The GUID, link, or username of the channel or group.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        chat_info = await self.get_chat_info(chat_guid)
        data = chat_info.to_dict() if hasattr(chat_info, 'to_dict') else chat_info

        voice_chat_id = None
        if 'chat' in data:
            voice_chat_id = data['chat'].get('group_voice_chat_id')
        elif 'group_voice_chat_id' in data:
            voice_chat_id = data.get('group_voice_chat_id')

        if not voice_chat_id:
            return Data({"status": "OK", "message": "No active voice chat found in this group/channel."})

        return await self.request(
            method = 'discardGroupVoiceChat',
            input = {
                'chat_guid': chat_guid,
                'voice_chat_id': voice_chat_id
            }
        )