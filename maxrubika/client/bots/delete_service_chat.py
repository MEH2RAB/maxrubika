import re
import maxrubika
from ..exceptions import InvalidInput

class DeleteServiceChat:
    async def delete_service_chat(
        self: "maxrubika.Client",
        service: str
    ):
        """
        Delete a service chat.

        Parameters:
            service (str): The GUID of the service chat to delete.

        Returns:
            The result of the API call.
        """
        if not re.match(r"^(s0)[a-zA-Z0-9]{30}$", service):
            raise InvalidInput("Invalid GUID format.")

        last_message = await self.get_last_message(service)
        last_data = last_message.to_dict() if hasattr(last_message, 'to_dict') else last_message

        message = last_data.get('message')

        if isinstance(message, dict):
            last_deleted_message_id = message.get('message_id', 0)
        else:
            last_deleted_message_id = 0

        return await self.request(
            method = 'deleteServiceChat',
            input = {
                'service_guid': service,
                'last_deleted_message_id': last_deleted_message_id
            }
        )