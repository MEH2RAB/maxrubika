import re
from pathlib import Path
from typing import Optional, Union, Dict, Any, Literal, List, TYPE_CHECKING

from .keypad_mixin import KeypadMixin
from .message_result import MessageResult

if TYPE_CHECKING:
    import maxrubika

_DEFAULT_NAMES = {
    "Voice": "voice.ogg",
    "Music": "music.mp3",
    "Image": "image.jpg",
    "Video": "video.mp4",
    "Gif": "gif.mp4"
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
    ) -> MessageResult:
        """
        Sends a file to a chat.

        Uploads the file (or uses a pre-uploaded `file_id`), builds the message
        payload, and dispatches a `sendFile` request.

        Parameters:
            chat_id (str): Target chat ID. Must match a user/bot/group/channel GUID or a username.
            file (str | bytes, optional): Path to file, URL, or raw bytes. Ignored if `file_id` or `base64` is provided.
            file_type (Literal['File', 'Image', 'Voice', 'Video', 'Music', 'Gif']): Type of file. Default is 'File'.
            text (str, optional): Caption text (Max: 2048 chars, 64 lines).
            file_id (str, optional): Already uploaded file_id (skips upload).
            base64 (str, optional): Base64 encoded file data.
            file_name (str, optional): Custom file name. If not provided, auto-generated based on `file` path or `file_type`.
            metadata (dict, optional): Pre-formatted metadata (Bold, Italic, etc.). Auto-generated from `text` if omitted.
            chat_keypad (Dict, optional): Custom keyboard attached to the message.
            inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
            reply_to_message_id (Union[int, str], optional): Message ID to reply to.
            disable_notification (bool): Disable notification. Default is False.
            resize_keyboard (bool): Resize keyboard vertically. Default is True.
            one_time_keyboard (bool): Hide keyboard after use. Default is False.

        Returns:
            Wrapper for the API response with message info and action methods
            (edit, delete, reply, forward).
        """
        from ..data import Data
        from .metadata import to_metadata
        from .exceptions import InvalidInput, MessageTooLong

        if not re.match(r"^(@[a-zA-Z0-9_]{3,32}|(c0|g0|b0)[a-zA-Z0-9]{30})$", chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if text is not None:
            if not isinstance(text, str):
                raise InvalidInput("'text' must be a string.")
            if len(text) > 2048:
                message = f"Caption is too long ({len(text)} characters). Maximum allowed is 2048."
                raise MessageTooLong(message)
            if text.count('\n') > 64:
                message = f"Caption has too many lines ({text.count(chr(10))}). Maximum allowed is 64."
                raise MessageTooLong(message)

        if not file_id:
            if file_name is None and isinstance(file, str) and not file.startswith(("http://", "https://")):
                path = Path(file)
                if file_type == "Voice":
                    file_name = path.stem + ".ogg"
                elif file_type == "Music":
                    file_name = path.stem + ".mp3"
                else:
                    file_name = path.name
            elif file_name is None:
                file_name = _DEFAULT_NAMES.get(file_type, "file.bin")

            file_id = await self.upload_file(
                file=file,
                base64=base64,
                file_name=file_name,
                file_type=file_type
            )

        if not file_id:
            raise InvalidInput("Either 'file', 'file_id', or 'base64' must be provided.")

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

        input_data = {
            'chat_id': chat_id,
            'file_id': file_id,
            'text': processed_text,
            'disable_notification': disable_notification,
            'file_type': file_type
        }

        if normalized_chat_keypad:
            normalized_chat_keypad['resize_keyboard'] = resize_keyboard
            normalized_chat_keypad['one_time_keyboard'] = one_time_keyboard
            input_data['chat_keypad'] = normalized_chat_keypad
            input_data['chat_keypad_type'] = 'New'

        if normalized_inline_keypad:
            input_data['inline_keypad'] = normalized_inline_keypad

        if reply_to_message_id is not None:
            input_data['reply_to_message_id'] = str(reply_to_message_id)

        if metadata:
            input_data['metadata'] = metadata

        input_data = {k: v for k, v in input_data.items() if v is not None}

        result = await self.request(
            method='sendFile',
            input=input_data
        )

        if isinstance(result, dict):
            result = Data(result)

        message_id = result.find_keys("message_id")
        message_id = str(message_id)

        return MessageResult(
            bot=self,
            chat_id=chat_id,
            message_id=message_id,
            result_data=result
        )