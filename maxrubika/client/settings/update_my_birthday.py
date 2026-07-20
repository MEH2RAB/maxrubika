from datetime import datetime
import re; import maxrubika
from ..exceptions import InvalidInput

class UpdateMyBirthday:
    async def update_my_birthday(
        self: "maxrubika.Client",
        birthday: str
    ):
        """
        Update the birthday in your profile.

        Parameters:
            birthday (str): Birthday in format YYYY-MM-DD (e.g., "2026-02-03")

        Returns:
            The updated user information.
        """
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', birthday):
            raise InvalidInput('birthday must be in format YYYY-MM-DD (e.g., "2026-02-03")')

        try:
            datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            raise InvalidInput('Invalid date. Please provide a valid date.')

        return await self.request(
            method = "updateProfile",
            input = {
                "birth_date": birthday,
                "updated_parameters": ["birth_date"]
            }
        )