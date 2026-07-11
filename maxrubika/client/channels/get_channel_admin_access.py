import maxrubika
from ..exceptions import InvalidInput

class GetChannelAdminAccess:
    async def get_channel_admin_access(
        self: "maxrubika.Client",
        channel: str,
        admin: str
    ):
        """
        Get the admin access list for a specific member in a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            admin (str): The GUID or username of the admin for whom admin access is being checked.

        Returns:
            The result of the API call.
        """
        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        member_guid = await self.get_guid(admin)

        if not member_guid.startswith(("u0", "b0")):
            message = f"'{admin}' does not point to a valid member. Expected a user GUID, bot GUID, or username."
            raise InvalidInput(message)

        return await self.request(
            method = 'getChannelAdminAccessList',
            input = {'channel_guid': channel_guid, 'member_guid': member_guid}
        )