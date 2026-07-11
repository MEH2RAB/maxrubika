import maxrubika
from ..exceptions import InvalidInput

class GetJoinLinks:
    async def get_join_links(self: "maxrubika.Client", chat: str):
        """
        Retrieves a list of join links for a specific group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the target group or channel.

        Returns:
            The API response containing the join links.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        return await self.request(method = 'getJoinLinks', input = {'object_guid': chat_guid})