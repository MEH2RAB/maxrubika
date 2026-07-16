from typing import Optional, Dict, List, Union
from datetime import datetime
import re
import maxrubika
from ..exceptions import InvalidInput

class UpdateMyProfile:
    async def update_my_profile(
        self: "maxrubika.Client",
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        bio: Optional[str] = None,
        birthday: Optional[str] = None,
        location: Optional[Dict[str, Union[float, Dict[str, Union[int, List[str], float]]]]] = None
    ):
        """
        Update user profile information.

        Parameters:
            first_name (Optional[str]): The updated first name.
            last_name (Optional[str]): The updated last name.
            bio (Optional[str]): The updated biography.
            birthday (str): Birthday in format YYYY-MM-DD (e.g., "2026-07-05").
            location (Optional[dict]): Location information containing:
                - longitude (float): Longitude coordinate.
                - latitude (float): Latitude coordinate.
                - map_view (dict): Map view details with:
                    - tile_side_count (int): Number of tile sides.
                    - tile_urls (List[str]): List of tile URLs.
                    - x_loc (float): X location on map.
                    - y_loc (float): Y location on map.

        Returns:
            The updated user information after the profile update.
        """
        if first_name is None and last_name is None and bio is None and birthday is None and location is None:
            message = "At least one parameter (first_name, last_name, bio, birthday, location) should be provided for update."
            raise InvalidInput(message)

        input = {'updated_parameters': []}

        if first_name is not None:
            if len(first_name) > 30:
                raise InvalidInput("'first_name' must be 30 characters or less.")
            input['updated_parameters'].append('first_name')
            input['first_name'] = first_name

        if last_name is not None:
            if len(last_name) > 50:
                raise InvalidInput("'last_name' must be 50 characters or less.")
            input['updated_parameters'].append('last_name')
            input['last_name'] = last_name

        if bio is not None:
            if len(bio) > 150:
                raise InvalidInput("'bio' must be 150 characters or less.")
            input['updated_parameters'].append('bio')
            input['bio'] = bio

        if birthday is not None:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', birthday):
                raise InvalidInput("birthday must be in format YYYY-MM-DD (e.g., '2026-02-03')")
            try:
                datetime.strptime(birthday, '%Y-%m-%d')
            except ValueError:
                raise InvalidInput("Invalid date. Please provide a valid date.")
            input['updated_parameters'].append('birth_date')
            input['birth_date'] = birthday

        if location is not None:
            input['updated_parameters'].append('location')
            input['location'] = location

        return await self.request(method = 'updateProfile', input = input)