import random
from typing import Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendLiveLocation:
    async def send_live_location(
        self: "maxrubika.Messenger",
        chat: str,
        latitude: float,
        longitude: float,
        live_period: int = 60,
        reply_to_message_id: Optional[Union[str, int]] = None
    ):
        """
        Send a live location.

        Parameters:
            chat (str): The GUID, link, or username of the chat, or 'me'/'cloud'/'self'/'myself'.
            latitude (float): Latitude (-90 to 90).
            longitude (float): Longitude (-180 to 180).
            live_period (int): Live location duration in seconds. Default: 60.
            reply_to_message_id (Optional[Union[str, int]]): The ID of the message to reply to. Defaults to None.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        if not isinstance(latitude, (int, float)):
            raise InvalidInput('latitude must be a number.')

        if not (-90 <= latitude <= 90):
            raise InvalidInput('latitude must be between -90 and 90 degrees.')

        if not isinstance(longitude, (int, float)):
            raise InvalidInput('longitude must be a number.')

        if not (-180 <= longitude <= 180):
            raise InvalidInput('longitude must be between -180 and 180 degrees.')

        if not isinstance(live_period, int) or live_period <= 0:
            raise InvalidInput('live_period must be a positive integer (seconds).')

        input_data = {
            'object_guid': chat_guid,
            'rnd': random.randint(100000, 999999),
            'live_location': {
                'current_location': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'map_view': {
                        'tile_side_count': 1,
                        'tile_urls': [],
                        'x_loc': 0.0,
                        'y_loc': 0.0
                    }
                },
                'live_period': live_period
            }
        }

        if reply_to_message_id is not None:
            input_data['reply_to_message_id'] = reply_to_message_id

        return await self.request(
            method='sendMessage',
            input=input_data
        )