import maxrubika
from ...data import Data

class GetMe:
    async def get_me(self: "maxrubika.Client"):
        """
        Get information about the authenticated user.

        Returns:
            Information about the authenticated user.
        """
        result = await self.get_user_info()

        data = result.to_dict() if hasattr(result, 'to_dict') else result

        if hasattr(self, 'auth') and self.auth:
            data['auth'] = self.auth

        if hasattr(self, 'private_key') and self.private_key:
            data['private_key'] = self.private_key

        return Data(data)