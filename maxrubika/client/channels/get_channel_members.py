from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChannelMembers:
    async def get_channel_members(
        self: "maxrubika.Messenger",
        channel: str,
        search_text: Optional[str] = None,
        start_id: Optional[str] = None
    ):
        """
        Get members in a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            search_text (str, optional): Text to search for in members. Defaults to None.
            start_id (str, optional): The ID to start fetching from. Defaults to None.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        input_data = {'channel_guid': channel_guid}

        if search_text:
            input_data['search_text'] = search_text.replace("@", "")

        if start_id:
            input_data['start_id'] = start_id

        return await self.request(method='getChannelAllMembers', input=input_data)