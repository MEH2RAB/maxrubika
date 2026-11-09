import json
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendMessage:
    @staticmethod
    def _parse_sse_data(raw: str) -> Dict[str, Any]:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def _build_payload(auth, client_info, message, session_id, is_support, generate_image):
        return {
            "api_version": "1",
            "auth": auth,
            "data": {
                "method": "sendMessage",
                "client": client_info,
                "input": {
                    "message": str(message),
                    "session_id": session_id,
                    "generate_image": generate_image,
                    "is_support": is_support
                }
            }
        }

    @staticmethod
    def _raise_on_server_error(event_name, data):
        from .exceptions import ServerError

        if event_name != "error":
            return

        error_data = data.get("data", {})
        error_value = error_data.get("status_det")

        if error_value == "SERVER_ERROR":

            message = "An error occurred on the AI server."
            raise ServerError(message)

    async def _stream_events(self, payload):
        import aiohttp

        buffer = bytearray()
        event_name = None
        data_lines = []

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            timeout=aiohttp.ClientTimeout(total=self.timeout),
        ) as session:
            async with session.post(self.base_url, json=payload) as resp:
                resp.raise_for_status()

                async for chunk in resp.content.iter_any():
                    if not chunk:
                        continue

                    buffer.extend(chunk)
                    start = 0

                    while True:
                        nl = buffer.find(b"\n", start)
                        if nl == -1:
                            break

                        line = bytes(buffer[start:nl]).decode().rstrip("\r")
                        start = nl + 1

                        if line.startswith("event:"):
                            event_name = line[6:].strip()
                        elif line.startswith("data:"):
                            data_lines.append(line[5:].strip())
                        elif line == "" and data_lines:
                            for value in data_lines:
                                yield {
                                    "event": event_name,
                                    "data": self._parse_sse_data(value),
                                }
                            event_name, data_lines = None, []

                    if start:
                        del buffer[:start]

    def _assemble_result(self, events):
        text = ""
        result = {}

        for event in events:
            name, data = event["event"], event["data"]

            if name == "createSession":
                session_obj = data.get("session", {})
                result["session_id"] = session_obj.get("session_id")
                result["title"] = session_obj.get("title")

            elif name == "createMessage":
                msg = data.get("message", {})
                result["message_id"] = msg.get("message_id")
                result["session_id"] = msg.get("session_id")

            elif name == "updateSession":
                if data.get("parameter_name") == "title":
                    result["title"] = data.get("set_value")

            elif name == "updateMessage":
                param = data.get("parameter_name")
                if not param:
                    continue
                if param == "text_content":
                    text += data.get("append_value", "")
                else:
                    result[param] = data.get("set_value") or data.get("append_value")

            elif name == "error":
                error_data = data.get("data", {})
                result["error"] = error_data.get("status_det")
                result["error_status"] = error_data.get("status")

        result["text_content"] = text
        return result

    async def send_message(
        self: "maxrubika.RubiAI",
        message: str,
        session_id: str = "",
        is_support: bool = False,
        generate_image: bool = False
    ):
        """
        Send a message to the AI service and return the assembled result.

        Parameters:
            message (str): Text message to send.
            session_id (str): Existing session ID to continue a conversation.
            is_support (bool): Whether the message is a support request.
            generate_image (bool): Whether to request image generation.

        Returns:
            Assembled result with text_content, title, session_id, message_id.
        """
        from ..data import Data

        payload = self._build_payload(
            self.auth, self.client_info,
            message, session_id, is_support, generate_image
        )

        events = []
        async for event in self._stream_events(payload):
            self._raise_on_server_error(event["event"], event["data"])
            events.append(event)

        result = self._assemble_result(events)

        if getattr(self, 'as_dict', False):
            return result

        return Data(result)