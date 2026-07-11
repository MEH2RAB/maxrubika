import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class SetVoiceChatSetting:
    async def set_voice_chat_setting(
        self: "maxrubika.Client",
        chat: str,
        title: str = None,
        join_muted: bool = None
    ):
        """
        Set voice chat settings for group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            title (str, optional): New title for voice chat.
            join_muted (bool, optional): Whether new participants join muted. (Only for groups)

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        is_group = chat_guid.startswith('g0')
        is_channel = chat_guid.startswith('c0')

        if is_channel and join_muted is not None:
            raise InvalidInput("'join_muted' parameter is only for groups, not channels.")

        chat_info = await self.get_chat_info(chat_guid)
        data = chat_info.to_dict() if hasattr(chat_info, 'to_dict') else chat_info

        voice_chat_id = data.get('chat', {}).get('group_voice_chat_id') or data.get('group_voice_chat_id')
        if not voice_chat_id:
            return Data({"status": "OK", "message": "No active voice chat found in this group/channel."})

        input = {
            'chat_guid': chat_guid,
            'voice_chat_id': voice_chat_id,
            'updated_parameters': []
        }
        if title:
            input['title'] = title
            input['updated_parameters'].append('title')

        if is_group and join_muted is not None:
            input['join_muted'] = join_muted
            input['updated_parameters'].append('join_muted')

        return await self.request(
            method = 'setGroupVoiceChatSetting',
            input = input
        )