from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetVoiceChatSetting:
    async def set_voice_chat_setting(
        self: "maxrubika.Messenger",
        chat: str,
        title: Optional[str] = None,
        join_muted: Optional[bool] = None,
        voice_chat_id: Optional[str] = None
    ):
        """
        Set voice chat settings for group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            title (Optional[str]): New title for voice chat.
            join_muted (Optional[bool]): Whether new participants join muted. (Only for groups)
            voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

        Returns:
            The result of the API call.
        """
        from ....data import Data
        from ...exceptions import InvalidInput, VoiceChatNotActive

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid group or channel. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        is_group = chat_guid.startswith('g0')
        is_channel = chat_guid.startswith('c0')

        if is_channel and join_muted is not None:
            raise InvalidInput("'join_muted' parameter is only for groups, not channels.")

        if not voice_chat_id:
            chat_info = await self.get_chat_info(chat_guid)
            data = Data(chat_info)
            voice_chat_id = data.find_keys("group_voice_chat_id")

            if not voice_chat_id:
                raise VoiceChatNotActive()

        input_data = {
            'chat_guid': chat_guid,
            'voice_chat_id': voice_chat_id,
            'updated_parameters': []
        }

        if title is not None:
            input_data['title'] = title
            input_data['updated_parameters'].append('title')

        if is_group and join_muted is not None:
            input_data['join_muted'] = join_muted
            input_data['updated_parameters'].append('join_muted')

        if not input_data['updated_parameters']:
            raise InvalidInput("At least one setting (title or join_muted) must be provided.")

        return await self.request(
            method='setGroupVoiceChatSetting',
            input=input_data
        )