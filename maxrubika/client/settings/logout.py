import sys
import maxrubika

class Logout:
    async def logout(
        self: "maxrubika.Client",
        confirm: bool = True
    ):
        """
        Log out of the current session.

        Parameters:
            confirm (bool): If True, ask the user for confirmation before
                logging out. If False, log out immediately.
                Default is True.

        Returns:
            The result of the logout operation if confirmed.
            Exits if cancelled.
        """
        if confirm:
            print("WARNING: This action will log you out of the current session.\n")

            while True:
                confirmation = input(
                    "Are you sure you want to logout? (y/n): "
                ).lower().strip()

                if confirmation == 'y':
                    print("Logging out...")
                    break
                elif confirmation == 'n':
                    print("Logout cancelled.")
                    sys.exit(0)
                else:
                    print("Invalid input. Please enter 'y' for yes or 'n' for no.")

        return await self.request(method = 'logout')