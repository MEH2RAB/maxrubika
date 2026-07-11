import maxrubika
from ..exceptions import InvalidInput

class RejectJoinRequest:
    async def reject_join_request(
        self: "maxrubika.Client",
        chat: str,
        user: str
    ):
        """
        Reject a join request for a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the group/channel.
            user (str): The user GUID or username of the requester.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        chat_type = 'Group' if chat_guid.startswith('g0') else 'Channel'

        input = {
            'object_guid': chat_guid,
            'object_type': chat_type,
            'user_guid': user_guid,
            'action': 'Reject'
        }
        return await self.request(method = 'actionOnJoinRequest', input = input)