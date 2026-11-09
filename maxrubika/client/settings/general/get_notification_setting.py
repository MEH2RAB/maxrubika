from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetNotificationSetting:
    async def get_notification_setting(self: "maxrubika.Messenger"):
        """
        Retrieves the current notification settings for the account.

        Returns:
            The result of the API call.
        """
        return await self.request(method='getNotificationSetting')