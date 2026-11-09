from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteAllMyGifSet:
    async def delete_all_my_gif_set(
        self: "maxrubika.Messenger"
    ):
        """
        Delete all GIFs from the user's personal GIF set.

        Returns:
            A result containing the deletion status and count.
        """
        from ...data import Data

        gifs_result = await self.get_my_gif_set()

        if isinstance(gifs_result, dict):
            gifs_result = Data(gifs_result)

        gifs = gifs_result.find_keys('gifs')

        if not gifs:
            result_dict = {
                "status": "OK",
                "message": "No GIFs found in your GIF set.",
                "deleted_count": 0
            }
            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)

        deleted_count = 0

        for gif in gifs:
            if isinstance(gif, dict):
                gif = Data(gif)

            file_id = gif.find_keys('file_id')
            if not file_id:
                continue

            await self.delete_my_gif_set(file_id)
            deleted_count += 1

        result_dict = {
            "status": "OK",
            "deleted_count": deleted_count,
            "total": len(gifs)
        }
        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)