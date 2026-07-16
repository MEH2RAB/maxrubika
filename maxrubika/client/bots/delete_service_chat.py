from typing import Union
import re; import maxrubika
from ..exceptions import InvalidInput

class DeleteServiceChat:
    async def delete_service_chat(
        self: "maxrubika.Client",
        service: str,
        last_deleted_message_id: Union[str, int]
    ):
        """
        Delete a service chat.

        Parameters:
            service_guid (str): The GUID of the service chat to delete.
            last_deleted_message_id (Union[str, int]): The last deleted message ID.

        Returns:
            The result of the API call.
        """
        if not re.match(r"^(s0)[a-zA-Z0-9]{30}$", service):
            raise InvalidInput("Invalid GUID format.")

        return await self.request(
            method = 'deleteServiceChat',
            input = {
                'service_guid': service,
                'last_deleted_message_id': last_deleted_message_id
            }
        )