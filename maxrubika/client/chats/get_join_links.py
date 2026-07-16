import maxrubika
from ..exceptions import InvalidInput

class GetJoinLinks:
    async def get_join_links(
        self: "maxrubika.Client",
        chat: str,
        creator: str = None
    ):
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

        input = {'object_guid': chat_guid}

        if creator:
            creator_guid = await self.get_guid(creator)
            if not creator_guid.startswith("u0"):
                message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            input['creator_guid'] = creator_guid
        return await self.request(method = 'getJoinLinks', input = input)