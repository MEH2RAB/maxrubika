from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetInfoByUsername:
    async def get_info_by_username(
        self: "maxrubika.Rubino",
        username: str
    ):
        """
        Get a page (user or channel) by its username.

        Parameters:
            username (str): The username to check.

        Returns:
            The result of the API call.
        """
        input_data = {
            'username': username.replace('@', ''),
            'profile_id': self.profile_id
        }

        method = 'getProfileByUsername' if self.api_version == 1 else 'isExistUsername'

        return await self.request(
            method=method,
            input=input_data
        )