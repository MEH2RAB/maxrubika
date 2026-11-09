from typing import Optional, Dict, List, Union, TYPE_CHECKING
from datetime import datetime
import re

if TYPE_CHECKING:
    import maxrubika

class UpdateMyProfile:
    async def update_my_profile(
        self: "maxrubika.Messenger",
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        bio: Optional[str] = None,
        birthday: Optional[str] = None,
        location: Optional[Dict[str, Union[float, Dict[str, Union[int, List[str], float]]]]] = None
    ):
        """
        Update user profile information.

        Parameters:
            first_name (str, optional): The updated first name (max 30 characters).
            last_name (str, optional): The updated last name (max 50 characters).
            bio (str, optional): The updated biography (max 150 characters).
            birthday (str, optional): Birthday in format YYYY-MM-DD (e.g., "2026-07-05").
            location (dict, optional): Location with keys: longitude (float), latitude (float), map_view (dict with tile_side_count, tile_urls, x_loc, y_loc).

        Returns:
            The updated user information after the profile update.
        """
        from ...exceptions import InvalidInput

        if first_name is None and last_name is None and bio is None and birthday is None and location is None:
            message = "At least one parameter (first_name, last_name, bio, birthday, location) should be provided for update."
            raise InvalidInput(message)

        input_data = {'updated_parameters': []}

        if first_name is not None:
            if len(first_name) > 30:
                raise InvalidInput("'first_name' must be 30 characters or less.")
            input_data['updated_parameters'].append('first_name')
            input_data['first_name'] = first_name

        if last_name is not None:
            if len(last_name) > 50:
                raise InvalidInput("'last_name' must be 50 characters or less.")
            input_data['updated_parameters'].append('last_name')
            input_data['last_name'] = last_name

        if bio is not None:
            if len(bio) > 150:
                raise InvalidInput("'bio' must be 150 characters or less.")
            input_data['updated_parameters'].append('bio')
            input_data['bio'] = bio

        if birthday is not None:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', birthday):
                raise InvalidInput("birthday must be in format YYYY-MM-DD (e.g., '2026-02-03')")
            try:
                datetime.strptime(birthday, '%Y-%m-%d')
            except ValueError:
                raise InvalidInput("Invalid date. Please provide a valid date.") from None
            input_data['updated_parameters'].append('birth_date')
            input_data['birth_date'] = birthday

        if location is not None:
            input_data['updated_parameters'].append('location')
            input_data['location'] = location

        return await self.request(method='updateProfile', input=input_data)