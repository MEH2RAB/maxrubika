from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetCurrentLiveLocation:
    async def set_current_live_location(
        self: "maxrubika.Messenger",
        longitude: float,
        latitude: float,
        tile_side_count: int = 1,
        tile_urls: Optional[List[str]] = None,
        x_loc: float = 0.0,
        y_loc: float = 0.0
    ):
        """
        Set the current live location.

        Parameters:
            longitude (float): Longitude coordinate.
            latitude (float): Latitude coordinate.
            tile_side_count (int, optional): Number of tiles per side. Default: 1.
            tile_urls (List[str], optional): URLs of map tiles. Defaults to empty list.
            x_loc (float, optional): X position on the map. Default: 0.0.
            y_loc (float, optional): Y position on the map. Default: 0.0.

        Returns:
            The result of the API call.
        """
        input_data = {
            'location': {
                'longitude': longitude,
                'latitude': latitude,
                'map_view': {
                    'tile_side_count': tile_side_count,
                    'tile_urls': tile_urls or [],
                    'x_loc': x_loc,
                    'y_loc': y_loc
                }
            }
        }

        return await self.request(
            method='setCurrentLiveLocation',
            input=input_data
        )