import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetProfileID:
    async def get_profile_id(
        self: "maxrubika.Rubino",
        username: str
    ) -> str:
        """
        Get profile ID by username or profile ID.

        Parameters:
            username (str): The username, profile ID, or 'me'.

        Returns:
            The profile ID string.
        """
        from ..data import Data
        from .exceptions import InvalidUsername

        username = username.replace('@', '')

        if username.lower() in ("me", "self", "myself"):
            return self.profile_id

        if re.match(r'^[0-9a-f]{24}$', username):
            return username

        result = await self.get_info_by_username(username)

        if isinstance(result, dict):
            result = Data(result)

        if self.api_version == 1:
            profile_data = result.find_keys('profile')
            if not profile_data:
                raise InvalidUsername()
            if isinstance(profile_data, dict):
                profile_data = Data(profile_data)
            profile_id = profile_data.find_keys('id')
            if not profile_id:
                raise InvalidUsername()
            return profile_id

        if result.find_keys('exist'):
            return result.find_keys('profile_id') or result.find_keys('id')

        raise InvalidUsername()