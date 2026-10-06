import re
from pathlib import Path
from typing import Optional, Union, Dict, Any, Literal, List
import maxrubika
from .metadata import to_metadata
from .keypad_mixin import KeypadMixin
from .exceptions import InvalidInput
from .message_result import MessageResult

_DEFAULT_NAMES = {
    "Voice": "voice.ogg",
    "Music": "music.mp3",
    "Image": "image.jpg",
    "Video": "video.mp4",
    "Gif": "gif.mp4",
}

class SendFile(KeypadMixin):
    async def send_file(
        self: "maxrubika.Bot",
        chat_id: str,
        file: Optional[Union[str, bytes]] = None,
        file_type: Literal['File', 'Image', 'Voice', 'Video', 'Music', 'Gif'] = 'File',
        text: Optional[str] = None,
        file_id: Optional[str] = None,
        base64: Optional[str] = None,
        file_name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        reply_to_message_id: Optional[Union[int, str]] = None,
        disable_notification: bool = False,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> Dict[str, Any]:
        """
        Sends a file to a chat.

        Parameters:
            chat_id (str): Target chat ID.
            file (str | bytes, optional): Path to file, URL, or raw bytes.
            file_type (str): Type of file ('File', 'Image', 'Voice', 'Video', 'Music', 'Gif').
            text (str, optional): Caption text.
            file_id (str, optional): Already uploaded file_id (skips upload).
            base64 (str, optional): Base64 encoded file data.
            file_name (str, optional): Custom file name. If not provided, auto-generated.
            metadata (dict, optional): Pre-formatted metadata (Bold, Italic, etc.).
            chat_keypad (Dict, optional): Custom keyboard attached to the message.
            inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
            reply_to_message_id (Union[int, str], optional): Message ID to reply to.
            disable_notification (bool): Disable notification.
            resize_keyboard (bool): Resize keyboard vertically.
            one_time_keyboard (bool): Hide keyboard after use.

        Returns:
            dict: API response with message information.
        """
        if not re.match(r"^(c0|g0|b0)[a-zA-Z0-9]{30}$", chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if not file_id:
            if file_name is None:
                if isinstance(file, str) and not file.startswith(("http://", "https://")):

                    path = Path(file)
                    if file_type == "Voice":
                        file_name = path.stem + ".ogg"
                    elif file_type == "Music":
                        file_name = path.stem + ".mp3"
                    else:
                        file_name = path.name
                else:
                    file_name = _DEFAULT_NAMES.get(file_type, "file.bin")

            upload_url = await self.request_send_file(file_type)

            file_id = await self.upload_file(
                url=upload_url,
                file=file,
                base64=base64,
                file_name=file_name
            )

        if not file_id:
            raise InvalidInput(
                "Either 'file', 'file_id', or 'base64' must be provided."
            )

        normalized_chat_keypad = self._normalize_keypad(chat_keypad, is_inline=False)
        normalized_inline_keypad = self._normalize_keypad(inline_keypad, is_inline=True)

        processed_text = text or ""
        if text and not metadata:
            try:
                processed = to_metadata(text)
                processed_text = processed["text"]
                metadata = processed.get("metadata")
            except Exception:
                processed_text = text
                metadata = None

        payload = {
            'chat_id': chat_id,
            'file_id': file_id,
            'text': processed_text,
            'disable_notification': disable_notification
        }
        if normalized_chat_keypad:
            normalized_chat_keypad['resize_keyboard'] = resize_keyboard
            normalized_chat_keypad['one_time_keyboard'] = one_time_keyboard
            payload['chat_keypad'] = normalized_chat_keypad
            payload['chat_keypad_type'] = 'New'

        if normalized_inline_keypad:
            payload['inline_keypad'] = normalized_inline_keypad

        if reply_to_message_id is not None:
            payload['reply_to_message_id'] = str(reply_to_message_id)

        if metadata:
            payload['metadata'] = metadata

        payload = {k: v for k, v in payload.items() if v is not None}

        result = await self.request('POST', 'sendFile', json = payload)

        message_id = result.find_keys("message_id")
        if message_id is not None:
            message_id = str(message_id)

        return MessageResult(
            bot=self,
            chat_id=chat_id,
            message_id=message_id,
            result_data=result
        )