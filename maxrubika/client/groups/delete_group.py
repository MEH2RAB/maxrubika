import sys
import maxrubika
from ..exceptions import InvalidInput

class DeleteGroup:
    async def delete_group(self: "maxrubika.Client", group: str):
        """
        Delete a group.

        Parameters:
            group (str): The GUID or link of the group.

        Returns:
            The result of the API call.
        """
        while True:
            print("WARNING: This action will permanently delete the group!")
            response = input("Are you sure? (y/n): ").strip().lower()

            if response == 'y':
                break
            if response == 'n':
                print("Operation cancelled.")
                sys.exit(0)
            print("Please enter 'y' for yes or 'n' for no.")

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        return await self.request(method = 'removeGroup', input = {'group_guid': group_guid})