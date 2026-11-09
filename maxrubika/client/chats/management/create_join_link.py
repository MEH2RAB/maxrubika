from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CreateJoinLink:
    async def create_join_link(
        self: "maxrubika.Messenger",
        chat: str,
        expire_time: Optional[int] = None,
        request_needed: bool = False,
        title: Optional[str] = None,
        usage_limit: int = 0
    ):
        """
        Creates an invite link for a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the target group or channel.
            expire_time (int, optional): The expiration time of the link in seconds.
            request_needed (bool): Whether join requests must be approved manually.
            title (str, optional): A custom title for the invite link.
            usage_limit (int): The maximum number of times the link can be used.

        Returns:
            The API response containing the created invite link.
        """
        from ...exceptions import InvalidInput

        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            message = f"'{chat}' does not point to a valid chat. Expected a chat GUID, chat link, or username."
            raise InvalidInput(message)

        if not isinstance(request_needed, bool):
            raise InvalidInput("'request_needed' must be of boolean type only.")

        input_data = {
            'object_guid': chat_guid,
            'request_needed': request_needed,
            'usage_limit': usage_limit
        }

        if isinstance(expire_time, int):
            input_data['expire_time'] = expire_time

        if isinstance(title, str):
            input_data['title'] = title

        return await self.request(method='createJoinLink', input=input_data)