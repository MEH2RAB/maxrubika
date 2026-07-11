import sys
import maxrubika

class Logout:
    async def logout(self: "maxrubika.Client"):
        """
        Print a warning and ask the user for confirmation before logging out.

        Returns:
            The result of the logout operation if confirmed.
            Exits if cancelled.
        """
        print("WARNING: This action will log you out of the current session.\n")

        while True:
            confirmation = input("Are you sure you want to logout? (y/n): ").lower().strip()

            if confirmation == 'y':
                print("Logging out...")
                return await self.request(method = 'logout')
            elif confirmation == 'n':
                print("Logout cancelled.")
                sys.exit(0)
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")