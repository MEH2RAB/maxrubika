import maxrubika
from ...data import Data

class DeleteAllMyGifSet:
    async def delete_all_my_gif_set(self: "maxrubika.Client"):
        """
        Delete all GIFs from the user's personal GIF set.

        Returns:
            Data: A Data object containing the deletion result.
        """
        gifs_result = await self.get_my_gif_set()
        gifs_data = gifs_result.to_dict() if hasattr(gifs_result, 'to_dict') else gifs_result

        gifs = gifs_data.get('gifs', [])

        if not gifs:
            return Data({"status": "OK", "message": "No GIFs found in your GIF set."})

        deleted_count = 0

        for gif in gifs:
            file_id = gif.get('file_id')
            if not file_id:
                continue
            try:
                await self.delete_my_gif_set(file_id)
                deleted_count += 1
            except Exception:
                pass

        return Data({
            "status": "OK",
            "deleted_count": deleted_count,
        })