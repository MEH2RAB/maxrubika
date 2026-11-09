from time import time
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetContactsUpdates:
    async def get_contacts_updates(
        self: "maxrubika.Messenger",
        state: Optional[Union[str, int]] = round(time()) - 150
    ):
        """
        Get updates related to contacts.

        Parameters:
            state (Union[str, int], optional): The state parameter to filter updates. Defaults to `round(time()) - 150`.

        Returns:
            The update related to contacts.
        """
        return await self.request(method='getContactsUpdates', input={'state': int(state)})