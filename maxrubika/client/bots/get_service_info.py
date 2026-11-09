import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetServiceInfo:
    async def get_service_info(self: "maxrubika.Messenger", service: str):
        """
        Get information about a service.

        Parameters:
            service (str): The GUID of the service.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        if not re.match(r"^(s0)[a-zA-Z0-9]{30}$", service):
            raise InvalidInput("Invalid GUID format.")

        return await self.request(method='getServiceInfo', input={'service_guid': service})