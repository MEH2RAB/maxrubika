from typing import Union, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CheckVoiceChatParticipants:
    async def check_voice_chat_participants(
        self: "maxrubika.Messenger",
        chat: str,
        users: Union[str, List[str]],
        voice_chat_id: Optional[str] = None
    ):
        """
        Check which of the given users/bots are currently in the group/channel voice chat.

        Parameters:
            chat (str): The GUID, link, or username of the group or channel.
            users (Union[str, List[str]]): A single user GUID, username, link, or a list of them.
            voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

        Returns:
            The result of the API call, containing only the participants from the provided list.
        """
        from ....data import Data
        from ...exceptions import InvalidInput, VoiceChatNotActive

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid group or channel. Expected a valid GUID, link, or username."
            raise InvalidInput(message)

        if isinstance(users, str):
            users = [users]

        user_guids = []
        for user in users:
            guid = await self.get_guid(user)
            user_guids.append(guid)

        if not voice_chat_id:
            chat_info = await self.get_chat_info(chat_guid)
            data = Data(chat_info)
            voice_chat_id = data.find_keys("group_voice_chat_id")

            if not voice_chat_id:
                raise VoiceChatNotActive()

        input_data = {
            'chat_guid': chat_guid,
            'voice_chat_id': voice_chat_id,
            'object_guids': user_guids
        }

        return await self.request(
            method='getGroupVoiceChatParticipantsByObjectGuids',
            input=input_data
        )