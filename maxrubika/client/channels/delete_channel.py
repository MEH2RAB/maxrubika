import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteChannel:
    async def delete_channel(
        self: "maxrubika.Messenger",
        channel: str,
        confirm: bool = True
    ):
        """
        Delete a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            confirm (bool): If True, ask for confirmation before deleting. Default is True.

        Returns:
            The result of the API call.
            Exits if cancelled.
        """
        from ..exceptions import InvalidInput

        if confirm:
            print("WARNING: This action will permanently delete the channel!")
            while True:
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

        return await self.request(
            method='removeChannel',
            input={'channel_guid': channel_guid}
        )