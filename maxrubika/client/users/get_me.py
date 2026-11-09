from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMe:
    async def get_me(self: "maxrubika.Messenger"):
        """
        Get information about the authenticated user.

        Returns:
            Information about the authenticated user.
        """
        from ...data import Data

        result = await self.get_user_info()

        data = result.to_dict() if isinstance(result, Data) else result

        if hasattr(self, 'auth') and self.auth:
            data['auth'] = self.auth

        if hasattr(self, 'private_key') and self.private_key:
            data['private_key'] = self.private_key

        if getattr(self, 'as_dict', False):
            return data
        return Data(data)