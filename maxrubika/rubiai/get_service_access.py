from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetServiceAccess:
    async def get_service_access(
        self: "maxrubika.RubiAI"
    ):
        """
        Retrieve the current AI service access information.

        Returns:
            Parsed service-access response.
        """
        return await self.request(method="getServiceAccess")