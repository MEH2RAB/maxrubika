from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class InviteToVoiceChat:
    async def invite_to_voice_chat(
        self: "maxrubika.Messenger",
        chat: str,
        invite_user: str,
        voice_chat_id: Optional[str] = None
    ):
        """
        Invite a user to a voice chat.

        Parameters:
            chat (str): The GUID, link, or username of the group or channel.
            invite_user (str): The GUID, username, or link of the user to invite.
            voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

        Returns:
            The result of the API call.
        """
        from ....data import Data
        from ...exceptions import InvalidInput, VoiceChatNotActive

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid group or channel. Expected a valid GUID, link, or username."
            raise InvalidInput(message)

        invite_user_guid = await self.get_guid(invite_user)

        if not invite_user_guid.startswith("u0"):
            message = f"'{invite_user}' does not point to a valid user. Expected a user GUID, username, or link."
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
            'invite_object_guid': invite_user_guid
        }

        return await self.request(
            method='inviteToGroupVoiceChat',
            input=input_data
        )