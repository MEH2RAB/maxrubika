from typing import Optional, Union, Dict, Any
import maxrubika

class SendMusic:
    async def send_music(
        self: "maxrubika.Bot",
        chat_id: str,
        music: Optional[str] = None,
        text: Optional[str] = None,
        file_id: Optional[str] = None,
        chat_keypad: Dict[str, Any] = None,
        inline_keypad: Dict[str, Any] = None,
        reply_to_message_id: Optional[Union[int, str]] = None,
        disable_notification: bool = False,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> Dict[str, Any]:
        """
        Sends a music to a chat.

        Parameters:
            chat_id (str): Target chat ID.
            music (str, optional): Path to the music file to upload and send.
            file_id (str, optional): Already uploaded file_id.
            text (str, optional): Caption text.
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
            file=music,
            file_id=file_id,
            file_type="Music",
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard
        )