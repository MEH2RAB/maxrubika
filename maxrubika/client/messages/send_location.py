from typing import Union
import random; import maxrubika
from ..exceptions import InvalidInput

class SendLocation:
    async def send_location(
        self: "maxrubika.Client",
        chat: str,
        latitude: float,
        longitude: float,
        reply_to_message_id: Union[str, int] = None
    ):
        """
        Send a map location.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            latitude (float): Latitude (-90 to 90).
            longitude (float): Longitude (-180 to 180).
            reply_to_message_id (Optional[Union[str, int]]): The ID of the message to which this is a reply. Defaults to None.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not isinstance(latitude, (int, float)):
            raise InvalidInput('latitude must be a number.')

        if not (-90 <= latitude <= 90):
            raise InvalidInput('latitude must be between -90 and 90 degrees.')

        if not isinstance(longitude, (int, float)):
            raise InvalidInput('longitude must be a number')

        if not (-180 <= longitude <= 180):
            raise InvalidInput('longitude must be between -180 and 180 degrees.')

        return await self.request(
            method = 'sendMessage',
            input = {
                'object_guid': chat_guid,
                'rnd': random.randint(100000, 999999),
                'location': {
                    'latitude': latitude,
                    'longitude': longitude
                    },
                'reply_to_message_id': reply_to_message_id
                }
            )