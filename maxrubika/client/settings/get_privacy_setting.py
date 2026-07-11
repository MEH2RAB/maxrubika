import maxrubika

class GetPrivacySetting:
    async def get_privacy_setting(self: "maxrubika.Client"):
        """
        Get the current user's privacy setting.

        Returns:
            The current user's privacy setting.
        """
        return await self.request(method = 'getPrivacySetting')