import asyncio
import pathlib
import logging
import maxrubika
from ..exceptions import InvalidInput, InvalidAccess

try:
    import aiortc
    from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
    from aiortc.contrib.media import MediaPlayer
except ImportError:
    aiortc = None
    RTCPeerConnection = None
    RTCSessionDescription = None
    MediaStreamTrack = None
    MediaPlayer = None

class VoiceChatConnection:
    def __init__(self, peer_connection, media_player, audio_track, chat_guid, voice_chat_id, client):
        self.pc = peer_connection
        self.player = media_player
        self.track = audio_track
        self.chat_guid = chat_guid
        self.voice_chat_id = voice_chat_id
        self.client = client
        self._speaking_task = None
        self._heartbeat_task = None

    def stop(self):
        if self.player and hasattr(self.player, 'audio'):
            self.player.audio.stop()
        if self.pc:
            asyncio.create_task(self.pc.close())
        if self._speaking_task:
            self._speaking_task.cancel()
        if self._heartbeat_task:
            self._heartbeat_task.cancel()

    def pause(self):
        if hasattr(self.track, 'pause'):
            self.track.pause()

    def resume(self):
        if hasattr(self.track, 'resume'):
            self.track.resume()

    def get_chat_info(self):
        return {
            "chat_guid": self.chat_guid,
            "voice_chat_id": self.voice_chat_id,
            "connection_state": self.pc.connectionState if self.pc else "Closed",
            "ice_state": self.pc.iceConnectionState if self.pc else "Closed",
        }

class PlayVoiceChat:
    logger = logging.getLogger("VoiceChatPlayer")

    async def _heartbeat(self: "maxrubika.Client", chat_guid: str) -> None:
        while True:
            try:
                await self.get_voice_chat_updates(chat_guid)
                self.logger.debug(f"[Heartbeat] Updated for {chat_guid}")
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                self.logger.info("[Heartbeat] Cancelled.")
                break
            except Exception as e:
                self.logger.error(f"[Heartbeat] Unexpected error: {e}")
                await asyncio.sleep(5)

    async def _speaking(self: "maxrubika.Client", chat_guid: str) -> None:
        while True:
            try:
                await self.send_voice_chat_activity(chat_guid)
                self.logger.debug(f"[Speaking] Activity sent for {chat_guid}")
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                self.logger.info("[Speaking] Cancelled.")
                break
            except Exception as e:
                self.logger.error(f"[Speaking] Unexpected error: {e}")
                await asyncio.sleep(2)

    async def play_voice_chat(
        self: "maxrubika.Client",
        chat: str,
        media: pathlib.Path
    ) -> VoiceChatConnection:
        """
        Plays voice media in a chat.

        Parameters:
            chat: The GUID, link, or username of the chat to play the voice media in.
            media: The path to the voice media file.
        """
        if aiortc is None:
            raise InvalidAccess(
                "aiortc library is not available. Install with: pip install aiortc"
            )

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        class AudioFileTrack(MediaStreamTrack):
            kind = "audio"

            def __init__(self, player):
                super().__init__()
                self.player = player
                self._paused = False

            async def recv(self):
                while self._paused:
                    await asyncio.sleep(0.1)
                return await self.player.audio.recv()

            def pause(self):
                self._paused = True

            def resume(self):
                self._paused = False

        chat_info = await self.get_chat_info(chat_guid)
        chat_data = chat_info.to_dict() if hasattr(chat_info, 'to_dict') else chat_info

        voice_chat_id = chat_data.get('chat', {}).get('group_voice_chat_id') or chat_data.get('group_voice_chat_id')

        if not voice_chat_id:
            self.logger.info(f"[VoiceChat] No active voice chat found. Starting new one...")
            voice_result = await self.start_voice_chat(chat_guid)
            voice_data = voice_result.to_dict() if hasattr(voice_result, 'to_dict') else voice_result
            voice_chat_id = voice_data.get('voice_chat_id') or voice_data.get('chat', {}).get('group_voice_chat_id')

        self.logger.info(f"[VoiceChat] Using voice chat ID: {voice_chat_id}")

        pc = RTCPeerConnection()
        media_player = MediaPlayer(str(media), decode=True)
        track = AudioFileTrack(media_player)
        pc.addTrack(track)

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        connect = await self.join_voice_chat(chat_guid, sdp_offer_data=offer.sdp)
        connect_data = connect.to_dict() if hasattr(connect, 'to_dict') else connect
        sdp_answer = connect_data.get('sdp_answer_data')
        
        if not sdp_answer:
            raise InvalidAccess("No SDP answer received from server.")

        await self.set_voice_chat_state(chat_guid, action="Unmute")

        connection = VoiceChatConnection(pc, media_player, track, chat_guid, voice_chat_id, self)
        connection._speaking_task = asyncio.create_task(self._speaking(chat_guid))
        connection._heartbeat_task = asyncio.create_task(self._heartbeat(chat_guid))

        await pc.setRemoteDescription(RTCSessionDescription(sdp_answer, "answer"))

        @pc.on("iceconnectionstatechange")
        def on_ice_change():
            self.logger.info(f"[ICE] State changed: {pc.iceConnectionState}")

        @pc.on("connectionstatechange")
        def on_conn_change():
            self.logger.info(f"[Connection] State changed: {pc.connectionState}")

        self.logger.info(f"[VoiceChat] Successfully connected to voice chat in {chat_guid}")

        return connection