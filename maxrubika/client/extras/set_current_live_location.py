from typing import List
import maxrubika

class SetCurrentLiveLocation:
    async def set_current_live_location(
        self: "maxrubika.Client",
        longitude: float,
        latitude: float,
        tile_side_count: int,
        tile_urls: List[str],
        x_loc: float,
        y_loc: float
    ):
        """
        Set the current live location.

        Parameters:
            longitude (float): Longitude coordinate.
            latitude (float): Latitude coordinate.
            tile_side_count (int): Number of tiles per side.
            tile_urls (List[str]): URLs of map tiles.
            x_loc (float): X position on the map.
            y_loc (float): Y position on the map.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'setCurrentLiveLocation',
            input = {
                'location': {
                    'longitude': longitude,
                    'latitude': latitude,
                    'map_view': {
                        'tile_side_count': tile_side_count,
                        'tile_urls': tile_urls,
                        'x_loc': x_loc,
                        'y_loc': y_loc
                    }
                }
            }
        )