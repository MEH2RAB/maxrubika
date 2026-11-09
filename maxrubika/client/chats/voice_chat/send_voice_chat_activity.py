from typing import Literal, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendVoiceChatActivity:
    async def send_voice_chat_activity(
        self: "maxrubika.Messenger",
        chat: str,
        activity: Literal['Speaking'] = 'Speaking',
        voice_chat_id: Optional[str] = None
    ):
        """
        Send voice chat activity (e.g., speaking).

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            activity (str): Activity type. Only 'Speaking' is allowed. Case-insensitive. Default: 'Speaking'.
            voice_chat_id (str, optional): Voice chat ID. If not provided, it will be fetched automatically.

        Returns:
            The result of the API call.
        """
        from ....data import Data
        from ...exceptions import InvalidInput, VoiceChatNotActive

        activity_map = {'speaking': 'Speaking'}
        normalized_activity = activity_map.get(str(activity).lower())

        if not normalized_activity:
            message = "'activity' must be 'Speaking'."
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
            'activity': normalized_activity
        }

        return await self.request(
            method='sendGroupVoiceChatActivity',
            input=input_data
        )