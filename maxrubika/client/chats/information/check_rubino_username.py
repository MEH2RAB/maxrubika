from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CheckRubinoUsername:
    async def check_rubino_username(
        self: "maxrubika.Messenger",
        username: str
    ):
        """
        Check the availability of a Rubino page.

        Parameters:
            username (str): The username to check.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='checkRubinoUsername',
            input={'username': username.replace('@', '')}
        )