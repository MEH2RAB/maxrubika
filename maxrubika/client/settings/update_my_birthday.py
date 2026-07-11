import maxrubika
from datetime import datetime
import re

class UpdateMyBirthday:
    async def update_my_birthday(
        self: "maxrubika.Client",
        birthday: str,
    ):
        """
        Update the birthday in your profile.

        Parameters:
            birthday (str): Birthday in format YYYY-MM-DD (e.g., "2026-02-03")
            
        Returns:
            maxrubika.types.Update: Update object confirming the change.
            
        Raises:
            ValueError: If birthday format is invalid.
        """
        
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', birthday):
            raise ValueError('birthday must be in format YYYY-MM-DD (e.g., "2026-02-03")')

        try:
            datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Invalid date. Please provide a valid date.')
        
        return await self.request(
            name = "updateProfile",
            input = {
                "birth_date": birthday,
                "updated_parameters": ["birth_date"]
            }
        )