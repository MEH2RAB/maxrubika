from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class TranscribeVoice:
    async def transcribe_voice(
        self: "maxrubika.Messenger",
        chat: Union[str, int],
        message_id: Union[str, int]
    ):
        """
        Transcribes voice messages.

        Parameters:
            chat (Union[str, int]): The GUID, link, or username of the chat containing the voice message.
            message_id (Union[str, int]): The ID of the voice message.

        Returns:
            The transcription result.
        """
        from ....data import Data
        from ...exceptions import ServerError

        chat_guid = await self.get_guid(chat)

        transcribe_input = {
            'object_guid': chat_guid,
            'message_id': message_id
        }

        transcribe_result = await self.request(
            method='transcribeVoice',
            input=transcribe_input
        )

        if isinstance(transcribe_result, dict):
            transcribe_result = Data(transcribe_result)

        transcription_id = transcribe_result.find_keys('transcription_id')

        if not transcription_id:
            message = "Failed to get transcription ID from transcribeVoice response."
            raise ServerError(message)

        transcription_input = {
            'message_id': message_id,
            'transcription_id': transcription_id
        }

        transcription_result = await self.request(
            method='getTranscription',
            input=transcription_input
        )

        if isinstance(transcription_result, dict):
            transcription_result = Data(transcription_result)

        result_dict = {
            "status": transcription_result.find_keys('status') or "OK",
            "text": transcription_result.find_keys('text') or "",
            "transcription_id": transcription_id
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)