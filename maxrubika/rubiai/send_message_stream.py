from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendMessageStream:
    async def send_message_stream(
        self: "maxrubika.RubiAI",
        message: str,
        session_id: str = "",
        is_support: bool = False,
        generate_image: bool = False
    ):
        """
        Send a message to the AI service and yield streamed events progressively.

        Parameters:
            message (str): Text message to send.
            session_id (str): Existing session ID to continue a conversation.
            is_support (bool): Whether the message is a support request.
            generate_image (bool): Whether to request image generation.

        Yields:
            Each parsed SSE event.
        """
        from ..data import Data

        payload = self._build_payload(
            self.auth, self.client_info,
            message, session_id, is_support, generate_image
        )

        async for event in self._stream_events(payload):
            self._raise_on_server_error(event["event"], event["data"])

            if getattr(self, 'as_dict', False):
                yield event
            else:
                yield Data(event)