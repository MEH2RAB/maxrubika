import maxrubika
from typing import Optional
from ..exceptions import InvalidInput

class UpdateMyName:
    async def update_my_name(
        self: "maxrubika.Client",
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ):
        """
        Update user's first name and/or last name.

        Parameters:
            first_name (Optional[str]): The updated first name (max 30 characters).
            last_name (Optional[str]): The updated last name (max 50 characters).

        Returns:
            The updated user information.
        """
        if first_name is None and last_name is None:
            raise InvalidInput('At least one parameter (first_name, last_name) should be provided for update.')

        input_data = {'updated_parameters': []}

        if first_name is not None:
            if len(first_name) > 30:
                raise InvalidInput('first_name must be 30 characters or less.')
            input_data['updated_parameters'].append('first_name')
            input_data['first_name'] = first_name

        if last_name is not None:
            if len(last_name) > 50:
                raise InvalidInput('last_name must be 50 characters or less.')
            input_data['updated_parameters'].append('last_name')
            input_data['last_name'] = last_name

        return await self.request(method = 'updateProfile', input = input_data)