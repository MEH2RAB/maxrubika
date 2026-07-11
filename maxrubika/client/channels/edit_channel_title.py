import maxrubika

class EditChannelTitle:
    async def edit_channel_title(
        self: "maxrubika.Client",
        channel: str,
        title: str
    ):
        """
        Edit title of a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            title (str): The new title of the channel.

        Returns:
            The result of the API call.
        """
        return await self.edit_channel_info(channel = channel, title = title)