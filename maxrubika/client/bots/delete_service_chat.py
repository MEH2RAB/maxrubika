from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteServiceChat:
    async def delete_service_chat(
        self: "maxrubika.Messenger",
        service: str
    ):
        """
        Delete a service chat.

        Parameters:
            service (str): The GUID of the service chat to delete.

        Returns:
            The result of the API call.
        """
        import re
        from ...data import Data
        from ..exceptions import InvalidInput

        if not re.match(r"^(s0)[a-zA-Z0-9]{30}$", service):
            raise InvalidInput("Invalid GUID format.")

        last_message = await self.get_last_message(service)

        if isinstance(last_message, dict):
            last_message = Data(last_message)

        last_deleted_message_id = last_message.find_keys('message_id') or 0

        input_data = {
            'service_guid': service,
            'last_deleted_message_id': last_deleted_message_id
        }

        return await self.request(
            method='deleteServiceChat',
            input=input_data
        )