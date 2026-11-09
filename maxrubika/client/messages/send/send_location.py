import random
from typing import Union, Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SendLocation:
    async def send_location(
        self: "maxrubika.Messenger",
        chat: str,
        latitude: float,
        longitude: float,
        reply_to_message_id: Optional[Union[str, int]] = None,
        map_view: Optional[Dict] = None
    ):
        """
        Send a map location.

        Parameters:
            chat (str): The GUID, link, or username of the chat, or 'me'/'cloud'/'self'/'myself'.
            latitude (float): Latitude (-90 to 90).
            longitude (float): Longitude (-180 to 180).
            reply_to_message_id (Union[str, int], optional): The ID of the message to which this is a reply.
            map_view (dict, optional): Custom map view with keys: tile_side_count (int), tile_urls (list[str]), x_loc (float), y_loc (float).
                Example:
                    map_view= {
                        "tile_side_count": 3,
                        "tile_urls": ["https://tile/...", ...],
                        "x_loc": 0.5,
                        "y_loc": 0.5
                    }

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

        input_data = {
            'object_guid': chat_guid,
            'rnd': random.randint(100000, 999999),
            'location': {
                'latitude': latitude,
                'longitude': longitude
            }
        }

        if map_view is not None:
            input_data['map_view'] = map_view

        if reply_to_message_id is not None:
            input_data['reply_to_message_id'] = reply_to_message_id

        return await self.request(method='sendMessage', input=input_data)