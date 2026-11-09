from typing import Literal, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetVoiceChatState:
    async def set_voice_chat_state(
        self: "maxrubika.Messenger",
        chat: str,
        action: Literal['Mute', 'Unmute', 'RequestSpeak', 'CancelRequestSpeak'] = 'Unmute',
        participant_chat_guid: Optional[str] = None,
        voice_chat_id: Optional[str] = None
    ):
        """
        Set group or channel voice chat state automatically.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            action (str): Action to apply. 'Mute', 'Unmute', 'RequestSpeak', or 'CancelRequestSpeak'. Case-insensitive. Default is 'Unmute'.
            participant_chat_guid (str, optional): Participant chat GUID. Default is self.guid.
            voice_chat_id (str, optional): Voice chat ID. If not provided, it will be fetched automatically.

        Returns:
            The result of the API call.
        """
        from ....data import Data
        from ...exceptions import InvalidInput, VoiceChatNotActive

        action_map = {
            'mute': 'Mute',
            'unmute': 'Unmute',
            'requestspeak': 'RequestSpeak',
            'cancelrequestspeak': 'CancelRequestSpeak'
        }

        normalized_action = action_map.get(str(action).lower())

        if not normalized_action:
            message = "'action' must be 'Mute', 'Unmute', 'RequestSpeak', or 'CancelRequestSpeak'."
            raise InvalidInput(message)

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
            'voice_chat_id': voice_chat_id,
            'action': normalized_action,
            'participant_object_guid': participant_chat_guid or self.guid
        }

        return await self.request(method='setGroupVoiceChatState', input=input_data)