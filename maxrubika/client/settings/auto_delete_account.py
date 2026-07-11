from typing import Union
import maxrubika

class AutoDeleteAccount:
    async def auto_delete_account(
        self: "maxrubika.Client",
        setting: Union[int, str]
    ):
        """
        Set account auto-deletion after months of inactivity.

        Parameters:
            setting (Union[int, str]): Months of inactivity. Accepts: 3, 6, 12, or 24.
                Can be int (3, 6, 12, 24) or str ("3", "6", "12", "24", "3m", "6m", "12m", "24m")

        Returns:
            The updated privacy settings.

        Examples:
            >>> await client.auto_delete_account(6)
            >>> await client.auto_delete_account("12m")
        """
        return await self.set_setting(inactive_account_delete = setting)