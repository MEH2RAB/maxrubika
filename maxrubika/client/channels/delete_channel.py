import sys
import maxrubika
from ..exceptions import InvalidInput

class DeleteChannel:
    async def delete_channel(self: "maxrubika.Client", channel: str):
        """
        Delete a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.

        Returns:
            The result of the API call.
        """
        while True:
            print("WARNING: This action will permanently delete the channel!")
            response = input("Are you sure? (y/n): ").strip().lower()

            if response == 'y':
                break
            elif response == 'n':
                print("Operation cancelled.")
                sys.exit(0)
            else:
                print("Please enter 'y' for yes or 'n' for no.")

        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        return await self.request(method = 'removeChannel', input = {'channel_guid': channel_guid})