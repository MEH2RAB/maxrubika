from typing import Optional
import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class JoinVoiceChat:
    async def join_voice_chat(
        self: "maxrubika.Client",
        chat: str,
        sdp_offer_data: Optional[str] = None
    ):
        """
        Join to the group | channel voice chat.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            sdp_offer_data (str, optional): SDP offer data. If not provided, uses default.

        Returns:
            The result of the API call.
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

        if sdp_offer_data is None:
            sdp_offer_data = """v=0
o=- 123456 2 IN IP4 127.0.0.1
s=-
c=IN IP4 0.0.0.0
t=0 0
m=audio 9 RTP/AVP 111
a=rtpmap:111 opus/48000/2
a=fmtp:111 minptime=10;useinbandfec=1
a=ice-ufrag:abc123
a=ice-pwd:xyz789
a=fingerprint:sha-256 12:34:56:78:9A:BC:DE:F0:12:34:56:78:9A:BC:DE:F0:12:34:56:78:9A:BC:DE:F0:12:34:56:78:9A
a=setup:actpass
a=mid:0"""

        return await self.request(
            method = 'joinGroupVoiceChat',
            input = {
                'chat_guid': chat_guid,
                'voice_chat_id': voice_chat_id,
                'sdp_offer_data': sdp_offer_data,
                'self_object_guid': self.guid
            }
        )