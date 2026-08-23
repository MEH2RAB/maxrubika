from typing import Optional, Union, Dict, Any
import maxrubika

class SendVideo:
    async def send_video(
        self: "maxrubika.Bot",
        chat_id: str,
        video: Optional[Union[str, bytes]] = None,
        text: Optional[str] = None,
        file_id: Optional[str] = None,
        base64: Optional[str] = None,
        file_name: Optional[str] = None,
        chat_keypad: Dict[str, Any] = None,
        inline_keypad: Dict[str, Any] = None,
        reply_to_message_id: Optional[Union[int, str]] = None,
        disable_notification: bool = False,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> Dict[str, Any]:
        """
        Sends a video to a chat.

        Parameters:
            chat_id (str): Target chat ID.
            video (str | bytes, optional): Path to the video file OR raw bytes.
            text (str, optional): Caption text.
            file_id (str, optional): Already uploaded file_id.
            base64 (str, optional): Base64 encoded video data.
            file_name (str, optional): Custom file name. If not provided, auto-generated.
            chat_keypad (Dict, optional): Custom keyboard attached to the message.
            inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
            reply_to_message_id (Union[int, str], optional): Message ID to reply to.
            disable_notification (bool): Disable notification.
            resize_keyboard (bool): Resize keyboard vertically.
            one_time_keyboard (bool): Hide keyboard after use.

        Returns:
            dict: API response with message information.
        """
        return await self.send_file(
            chat_id=chat_id,
            file=video,
            file_id=file_id,
            file_type="Video",
            text=text,
            base64=base64,
            file_name=file_name,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard
        )