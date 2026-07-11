import maxrubika

class DeleteMyGifSet:
    async def delete_my_gif_set(self: "maxrubika.Client", file_id: str):
        """
        Deletes a GIF from the user's personal GIF set.

        Parameters:
            file_id (str): The file ID of the GIF to be removed.

        Returns:
            The result of the API call.
        """
        return await self.request(method = 'removeFromMyGifSet', input = {'file_id': file_id})