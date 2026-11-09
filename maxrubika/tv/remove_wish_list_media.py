from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class RemoveWishListMedia:
    async def remove_wish_list_media(
        self: "maxrubika.RubikaTV",
        media_id: str,
        track_id: Optional[str] = None
    ):
        """
        Remove a media from the wishlist.

        Parameters:
            media_id (str): Identifier of the media.
            track_id (str, optional): Optional tracking identifier.

        Returns:
            The API output.
        """
        input_data = {
            "action": "RemoveWishList",
            "media_id": media_id
        }

        if track_id is not None:
            input_data["track_id"] = track_id

        return await self.request(
            method="actionOnMedia",
            input=input_data
        )