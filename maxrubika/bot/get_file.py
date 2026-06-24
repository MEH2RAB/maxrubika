import maxrubika

class GetFile:
    async def get_file(self: "maxrubika.Bot", file_id: str):
        """
        Requests the file associated with the specified file ID.

        Parameters:
            file_id (str): The identifier of the file to retrieve. This should be a valid file ID within the system.
        """
        payload = {'file_id': file_id}

        return await self._request('POST', 'getFile', json = payload)