from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SearchLocation:
    async def search_location(
        self: "maxrubika.Rubino",
        usage: Literal['Search', 'AddPost'] = 'Search',
        search_text: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Search for locations.

        Parameters:
            usage (Literal['Search', 'AddPost']): The search usage context. Case-sensitive.
            search_text (str, optional): The search text for the location. Required when 'usage' is 'Search'. Defaults to None.
            latitude (float, optional): The latitude for location bias. Required when 'usage' is 'AddPost'. Defaults to None.
            longitude (float, optional): The longitude for location bias. Required when 'usage' is 'AddPost'. Defaults to None.
            start_id (str, optional): The starting location ID for pagination. Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        if usage == 'Search':
            if not search_text or not search_text.strip():
                message = "'search_text' is required when 'usage' is 'Search'."
                raise InvalidInput(message)
        elif usage == 'AddPost':
            if latitude is None or longitude is None:
                message = "'latitude' and 'longitude' are required when 'usage' is 'AddPost'."
                raise InvalidInput(message)
        else:
            message = "'usage' must be 'Search' or 'AddPost'."
            raise InvalidInput(message)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'usage': usage
        }

        if search_text is not None:
            input_data['search_text'] = search_text

        if latitude is not None and longitude is not None:
            input_data['search_location'] = {
                'latitude': latitude,
                'longitude': longitude
            }

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='searchLocation',
            input=input_data
        )