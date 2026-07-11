import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class GetVoiceChatParticipants:
    async def get_voice_chat_participants(
        self: "maxrubika.Client",
        chat: str,
        show_user_guids: bool = False
    ):
        """
        Get list of participants in a voice chat.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            show_user_guids (bool, optional): Show user GUIDs in output. Default is False.

        Returns:
            The result containing all voice chat participants with total count.
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

        start_id = None
        total = 0
        all_participants = []
        user_guids = set()

        while True:
            result = await self.request(
                method = 'getGroupVoiceChatParticipants',
                input = {
                    'chat_guid': chat_guid,
                    'voice_chat_id': voice_chat_id,
                    'start_id': start_id
                }
            )
            data = result.to_dict() if hasattr(result, 'to_dict') else result

            if not data or not isinstance(data, dict):
                break

            participants = data.get('participants', [])
            if not participants:
                break

            for participant in participants:
                user_guid = participant.get('user_guid')
                if user_guid and user_guid not in user_guids:
                    user_guids.add(user_guid)
                    all_participants.append(participant)
                    total += 1

            has_continue = data.get('has_continue', False)
            if not has_continue:
                break

            next_start_id = data.get('next_start_id')
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