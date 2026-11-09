from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetStickerSetting:
    async def get_sticker_setting(self: "maxrubika.Messenger"):
        """
        Get the sticker settings of the current user.

        Returns:
            The result of the API call containing sticker settings.
        """
        return await self.request(method='getStickerSetting')