import maxrubika

class DeleteFolder:
    """
    Provides a method to delete a folder.

    Methods:
        delete_folder: Delete a folder.

    Attributes:
        self (maxrubika.Client): The maxrubika client instance.
    """

    async def delete_folder(
            self: "maxrubika.Client",
            folder_id: str
    ) -> "maxrubika.types.Update":
        """
        Delete a folder.
        
        Parameters:
            folder_id (str): The ID of the folder to be deleted.

        Returns:
            maxrubika.types.Update: Result of the delete folder operation.
        """
        return await self.request(name = 'deleteFolder', input = {'folder_id': str(folder_id)})