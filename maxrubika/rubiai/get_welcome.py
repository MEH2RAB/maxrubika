from typing import Literal, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetWelcome:
    async def get_welcome(
        self: "maxrubika.RubiAI",
        location: Literal["VOD", "Home", "Messenger", "Social"] = "Messenger",
        location_id: str = ""
    ):
        """
        Retrieve welcome information for a specified application location.

        Parameters:
            location (str): Application location. Case-insensitive.
                Accepts: 'VOD', 'Home', 'Messenger', 'Social'.
            location_id (str): Optional identifier of the location.

        Returns:
            The API response.
        """
        from .exceptions import InvalidInput

        location_map = {
            'vod': 'VOD',
            'home': 'Home',
            'messenger': 'Messenger',
            'social': 'Social'
        }

        normalized_location = location_map.get(str(location).lower())

        if not normalized_location:
            message = "'location' must be 'VOD', 'Home', 'Messenger', or 'Social'."
            raise InvalidInput(message)

        input_data = {
            "location": normalized_location,
            "location_id": location_id
        }

        return await self.request(
            method="getWelcome",
            input=input_data
        )