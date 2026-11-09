from typing import Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CheckChannelsWithUsername:
    async def check_channels_with_username(
        self: "maxrubika.Messenger",
        usernames: Union[str, List[str]]
    ):
        """
        Check which channels have the given usernames.

        Parameters:
            usernames (Union[str, List[str]]): A single username or a list of usernames.

        Returns:
            The result of the API call.
        """
        if isinstance(usernames, str):
            usernames = [usernames]

        usernames = [u.replace('@', '') for u in usernames]

        return await self.request(
            method='checkChannelsWithUsername',
            input={'usernames': usernames}
        )