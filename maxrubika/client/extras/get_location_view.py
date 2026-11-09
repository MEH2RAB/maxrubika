from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetLocationView:
    async def get_location_view(
        self: "maxrubika.Messenger",
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
        from ..exceptions import InvalidInput

        if not isinstance(latitude, (int, float)):
            raise InvalidInput('latitude must be a number.')

        if not (-90 <= latitude <= 90):
            raise InvalidInput('latitude must be between -90 and 90 degrees.')

        if not isinstance(longitude, (int, float)):
            raise InvalidInput('longitude must be a number.')

        if not (-180 <= longitude <= 180):
            raise InvalidInput('longitude must be between -180 and 180 degrees.')

        input_data = {
            'location': {
                'latitude': latitude,
                'longitude': longitude
            }
        }
        return await self.request(
            method='getMapView',
            input=input_data
        )