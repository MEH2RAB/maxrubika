import re
from datetime import datetime
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UpdateMyBirthday:
    async def update_my_birthday(
        self: "maxrubika.Messenger",
        birthday: Union[str, datetime]
    ):
        """
        Update the birthday in your profile.

        Parameters:
            birthday (Union[str, datetime]): Birthday in format YYYY-MM-DD (e.g., "2026-02-03") or a datetime object.

        Returns:
            The updated user information.
        """
        from ...exceptions import InvalidInput

        if isinstance(birthday, datetime):
            birthday = birthday.strftime('%Y-%m-%d')

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', birthday):
            raise InvalidInput('birthday must be in format YYYY-MM-DD (e.g., "2026-02-03")')

        try:
            datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            raise InvalidInput('Invalid date. Please provide a valid date.') from None

        input_data = {
            "birth_date": birthday,
            "updated_parameters": ["birth_date"]
        }

        return await self.request(method="updateProfile", input=input_data)