from typing import Union
from time import time
import maxrubika

class GetFolders:
    async def get_folders(
        self: "maxrubika.Client",
        last_state: Union[int, str] = round(time()) - 150
    ):
        """
        Get a list of folders.

        Parameters:
            last_state (Union[int, str]): The last state to retrieve folders.

        Returns:
            List of folders.
        """
        return await self.request(method = 'getFolders', input = {'last_state': int(last_state)})