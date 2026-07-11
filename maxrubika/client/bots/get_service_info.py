import re; import maxrubika
from ..exceptions import InvalidInput

class GetServiceInfo:
    async def get_service_info(self: "maxrubika.Client", service: str):
        """
        Get information about a service.

        Parameters:
            service (str): The GUID of the service.

        Returns:
            The result of the API call.
        """
        if not re.match(r"^(s0)[a-zA-Z0-9]{30}$", service):
            raise InvalidInput("Invalid GUID format.")

        return await self.request(method = 'getServiceInfo', input = {'service_guid': service})