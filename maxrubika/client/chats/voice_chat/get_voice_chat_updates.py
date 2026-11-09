from time import time
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetVoiceChatUpdates:
    async def get_voice_chat_updates(
        self: "maxrubika.Messenger",
        chat: str,
        voice_chat_id: Optional[str] = None,
        state: Optional[Union[int, str]] = None
    ):
        """
        Get voice chat updates for a group.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.
            state (Union[int, str], optional): The state for updates. If not provided, it defaults to the current time minus 150 seconds.

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

        if state is None:
            state = str(round(time()) - 150)

        input_data = {
            'chat_guid': chat_guid,
            'voice_chat_id': voice_chat_id,
            'state': state
        }

        return await self.request(
            method='getGroupVoiceChatUpdates',
            input=input_data
        )