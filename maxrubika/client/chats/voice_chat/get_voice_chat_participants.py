from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetVoiceChatParticipants:
    async def get_voice_chat_participants(
        self: "maxrubika.Messenger",
        chat: str,
        show_user_guids: bool = False,
        voice_chat_id: Optional[str] = None,
        all_pages: bool = True,
        start_id: Optional[str] = None
    ):
        """
        Get list of participants in a voice chat.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            show_user_guids (bool, optional): Show user GUIDs in output. Default is False.
            voice_chat_id (str, optional): Voice chat ID. If not provided, it will be fetched automatically.
            all_pages (bool, optional): If True, fetch all pages. If False, only one page using start_id. Default is True.
            start_id (str, optional): Starting participant ID for pagination. Only used when all_pages is False.

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

        if not all_pages:
            input_data = {
                'chat_guid': chat_guid,
                'voice_chat_id': voice_chat_id
            }
            if start_id is not None:
                input_data['start_id'] = start_id

            return await self.request(
                method='getGroupVoiceChatParticipants',
                input=input_data
            )

        total = 0
        all_participants = []
        user_guids = set()

        while True:
            input_data = {
                'chat_guid': chat_guid,
                'voice_chat_id': voice_chat_id
            }
            if start_id is not None:
                input_data['start_id'] = start_id

            result = await self.request(
                method='getGroupVoiceChatParticipants',
                input=input_data
            )

            result_data = Data(result)
            participants = result_data.find_keys('participants')

            if not participants:
                break

            for participant in participants:
                p_data = Data(participant)
                user_guid = p_data.find_keys('user_guid') or p_data.find_keys('participant_object_guid_type')

                if user_guid and user_guid not in user_guids:
                    user_guids.add(user_guid)
                    all_participants.append(p_data.to_dict())
                    total += 1

            has_continue = result_data.find_keys('has_continue')
            if not has_continue:
                break

            next_start_id = result_data.find_keys('next_start_id')
            if not next_start_id or next_start_id == start_id:
                break

            start_id = str(next_start_id)

        result_dict = {
            "participants": all_participants,
            "total": total,
            "voice_chat_id": voice_chat_id,
            "chat_guid": chat_guid
        }
        if show_user_guids:
            result_dict["user_guids"] = list(user_guids)

        return Data(result_dict)