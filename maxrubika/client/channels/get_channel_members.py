import maxrubika
from ..exceptions import InvalidInput

class GetChannelMembers:
    async def get_channel_members(
        self: "maxrubika.Client",
        channel: str,
        search_text: str = None,
        start_id: str = None
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
        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        input = {'channel_guid': channel_guid}

        if search_text:
            input['search_text'] = search_text.replace("@", "")

        if start_id:
            input['start_id'] = start_id

        return await self.request(method = 'getChannelAllMembers', input = input)