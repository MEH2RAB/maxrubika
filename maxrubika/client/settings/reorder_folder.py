from typing import Union, List
import maxrubika

class ReorderFolder:
    async def reorder_folder(
        self: "maxrubika.Client",
        folder_ids: Union[str, List[str]]
    ):
        """
        Reorder folders.

        Parameters:
            folder_ids (Union[str, List[str]]): A single folder ID or a list of folder IDs in the new order.

        Returns:
            The result of the API call.
        """
        if isinstance(folder_ids, str):
            folder_ids = [folder_ids]

        return await self.request(
            method = 'reorderFolder',
            input = {'folder_ids': folder_ids}
        )