from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetListItems:
    async def get_list_items(
        self: "maxrubika.RubikaTV",
        list_id: str,
        type: Literal["Media", "LinkItem", "Cast"] = "Media",
        is_channel: Optional[bool] = None,
        start_id: Optional[str] = None
    ):
        """
        Retrieve items from a VOD list.

        Parameters:
            list_id (str): Identifier of the list.
            type (str): Type of items: "Media", "LinkItem", or "Cast". Case-insensitive.
            is_channel (bool, optional): Optional channel filter.
            start_id (str, optional): Starting item ID for pagination.

        Returns:
            The API output.
        """
        from .exceptions import InvalidInput

        type_map = {
            'media': 'Media',
            'linkitem': 'LinkItem',
            'link_item': 'LinkItem',
            'cast': 'Cast'
        }

        normalized_type = type_map.get(str(type).lower())

        if not normalized_type:
            message = "'type' must be 'Media', 'LinkItem', or 'Cast'."
            raise InvalidInput(message)

        track_id = None
        if ";" in list_id:
            list_id, track_id = list_id.split(";", 1)

        input_data = {
            "list_id": list_id,
            "type": normalized_type
        }

        if track_id is not None:
            input_data["track_id"] = track_id

        if is_channel is not None:
            input_data["is_channel"] = is_channel

        if start_id is not None:
            input_data["start_id"] = start_id

        return await self.request(
            method="getListItems",
            input=input_data
        )