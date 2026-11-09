from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetFile:
    async def get_file(self: "maxrubika.Bot", file_id: str):
        """
        Requests the file associated with the specified file ID.

        Parameters:
            file_id (str): The identifier of the file to retrieve.

        Returns:
            The API response with file information.
        """
        return await self.request(
            method='getFile',
            input={'file_id': file_id}
        )