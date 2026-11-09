from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetUserSetting:
    async def get_user_setting(self: "maxrubika.Messenger"):
        """
        Get user account settings, similar to `get_privacy_setting`.

        Returns:
            The result of the API call. Includes the `privacy_setting` object (same as `get_privacy_setting`) plus an additional `access_list`.
        """
        return await self.request(method='getUserSetting')