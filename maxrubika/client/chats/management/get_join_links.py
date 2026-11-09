from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetJoinLinks:
    async def get_join_links(
        self: "maxrubika.Messenger",
        chat: str,
        creator: Optional[str] = None
    ):
        """
        Retrieves a list of join links for a specific group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the target group or channel.
            creator (str, optional): The user GUID or username of the link creator to filter by.

        Returns:
            The API response containing the join links.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        input_data = {'object_guid': chat_guid}

        if creator:
            creator_guid = await self.get_guid(creator)
            if not creator_guid.startswith("u0"):
                message = f"'{creator}' does not point to a valid user. Expected a user GUID or username."
                raise InvalidInput(message)
            input_data['creator_guid'] = creator_guid

        return await self.request(method='getJoinLinks', input=input_data)