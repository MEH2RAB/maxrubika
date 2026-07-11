import maxrubika
from ..exceptions import InvalidInput

class GetLocationView:
    async def get_location_view(
        self: "maxrubika.Client",
        latitude: float,
        longitude: float
    ):
        """
        Get map view for a location.

        Parameters:
            latitude (float): Latitude (-90 to 90)
            longitude (float): Longitude (-180 to 180)

        Returns:
            Map view data.
        """
        if not isinstance(latitude, (int, float)):
            raise InvalidInput('latitude must be a number.')

        if not (-90 <= latitude <= 90):
            raise InvalidInput('latitude must be between -90 and 90 degrees.')

        if not isinstance(longitude, (int, float)):
            raise InvalidInput('longitude must be a number.')

        if not (-180 <= longitude <= 180):
            raise InvalidInput('longitude must be between -180 and 180 degrees.')

        return await self.request(
            method = 'getMapView',
            input = {
                'location': {
                    'latitude': latitude,
                    'longitude': longitude
                    }
                }
            )