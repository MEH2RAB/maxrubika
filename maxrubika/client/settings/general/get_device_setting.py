from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetDeviceSetting:
    async def get_device_setting(self: "maxrubika.Messenger"):
        """
        Get all device settings (data, appearance, and notification).

        Returns:
            The result of the API call, containing `data_setting`, `appearance_setting`, and `notification_setting`.
        """
        return await self.request(method='getDeviceSetting')