from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class JoinVoiceChat:
    async def join_voice_chat(
        self: "maxrubika.Messenger",
        chat: str,
        sdp_offer_data: Optional[str] = None,
        voice_chat_id: Optional[str] = None
    ):
        """
        Join a group/channel voice chat.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            sdp_offer_data (Optional[str]): SDP offer data. If not provided, uses a default dummy SDP.
            voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

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

        if sdp_offer_data is None:
            sdp_offer_data = (
                "v=0\n"
                "o=- 123456 2 IN IP4 127.0.0.1\n"
                "s=-\n"
                "c=IN IP4 0.0.0.0\n"
                "t=0 0\n"
                "m=audio 9 RTP/AVP 111\n"
                "a=rtpmap:111 opus/48000/2\n"
                "a=fmtp:111 minptime=10;useinbandfec=1\n"
                "a=ice-ufrag:abc123\n"
                "a=ice-pwd:xyz789\n"
                "a=fingerprint:sha-256 12:34:56:78:9A:BC:DE:F0:12:34:56:78:9A:BC:DE:F0:12:34:56:78:9A:BC:DE:F0:12:34:56:78:9A\n"
                "a=setup:actpass\n"
                "a=mid:0"
            )

        input_data = {
            'chat_guid': chat_guid,
            'voice_chat_id': voice_chat_id,
            'sdp_offer_data': sdp_offer_data,
            'self_object_guid': self.guid
        }

        return await self.request(
            method='joinGroupVoiceChat',
            input=input_data
        )