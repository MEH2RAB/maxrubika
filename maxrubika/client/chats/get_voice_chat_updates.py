from time import time
import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class GetVoiceChatUpdates:
    async def get_voice_chat_updates(
        self: "maxrubika.Client",
        chat: str,
        state: int = None
    ):
        """
        Get voice chat updates for a group.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            state (int, optional): The state for updates. If not provided, it defaults to the current time minus 150 seconds.

        Returns:
            Update group containing the voice chat updates.
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

        if state is None:
            state = round(time()) - 150

        return await self.request(
            method = 'getGroupVoiceChatUpdates',
            input = {
                'chat_guid': chat_guid,
                'voice_chat_id': voice_chat_id,
                'state': state
            }
        )