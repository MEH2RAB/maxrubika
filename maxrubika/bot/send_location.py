import re
from typing import Union, Dict, Any, Optional, List
import maxrubika
from .keypad_mixin import KeypadMixin
from .exceptions import InvalidInput

class Sendlocation(KeypadMixin):
    async def send_location(
        self: "maxrubika.Bot",
        chat_id: str,
        latitude: float,
        longitude: float,
        chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        reply_to_message_id: Optional[Union[int, str]] = None,
        disable_notification: bool = False,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> Dict[str, Any]:
        """
        Sends a location message to a chat.

        Parameters:
            chat_id (str): chat_id for the target chat.
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.
            chat_keypad (Dict[str, Any], optional): Custom keyboard attached to the message. Defaults to None.
            inline_keypad (Dict[str, Any], optional): Custom inline keyboard attached to the message. Defaults to None.
            reply_to_message_id (Union[int, str], optional): If the message is a reply, the original message's ID. Defaults to None.
            disable_notification (bool, optional): Sends the message silently. Users will not receive a notification. Defaults to False.
            resize_keyboard (bool, optional): Requests clients to resize the keyboard vertically. Defaults to True.
            one_time_keyboard (bool, optional): Requests clients to hide the keyboard as soon as it's been used. Defaults to False.

        Returns:
            dict: API response with message information.
        """
        if not re.match(r"^(c0|g0|b0)[a-zA-Z0-9]{30}$", chat_id):
            raise InvalidInput("Invalid 'chat_id' format.")

        if not isinstance(latitude, (int, float)):
            raise InvalidInput("'latitude' must be a number.")

        if not (-90 <= latitude <= 90):
            raise InvalidInput("'latitude' must be between -90 and 90 degrees.")

        if not isinstance(longitude, (int, float)):
            raise InvalidInput("'longitude' must be a number.")

        if not (-180 <= longitude <= 180):
            raise InvalidInput("'longitude' must be between -180 and 180 degrees.")

        normalized_chat_keypad = self._normalize_keypad(chat_keypad, is_inline=False)
        normalized_inline_keypad = self._normalize_keypad(inline_keypad, is_inline=True)

        payload: Dict[str, Any] = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
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
            payload['reply_to_message_id'] = reply_to_message_id

        payload = {k: v for k, v in payload.items() if v is not None}
        return await self._request('POST', 'sendLocation', json = payload)