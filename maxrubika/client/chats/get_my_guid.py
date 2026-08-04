import maxrubika

class GetMyGuid:
    async def get_my_guid(self: "maxrubika.Client"):
        """
        Get the GUID of the currently authenticated user.

        Returns:
            str: The user's GUID.
        """
        return self.guid