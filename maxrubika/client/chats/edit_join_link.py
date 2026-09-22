from typing import Optional
import maxrubika
from ..exceptions import InvalidInput

class EditJoinLink:
    async def edit_join_link(
        self: "maxrubika.Client",
        chat: str,
        join_link: str,
        title: Optional[str] = None,
        expire_time: Optional[int] = None,
        request_needed: Optional[bool] = None,
        usage_limit: Optional[int] = None
    ):
        """
        Edit an existing invite link for a group or channel.

        Parameters:
            chat (str): The GUID, link, or username of the target group or channel.
            join_link (str): The join link to edit.
            expire_time (Optional[int]): The new expiration time of the link in seconds.
            request_needed (Optional[bool]): Whether join requests must be approved manually.
            title (Optional[str]): A new custom title for the invite link.
            usage_limit (Optional[int]): The new maximum number of times the link can be used.

        Returns:
            The API response containing the edited invite link.
        """
        chat_guid = await self.get_guid(chat)

        if not chat_guid.startswith(("g0", "c0")):
            raise InvalidInput(
                f"'{chat}' does not point to a valid chat. Expected a group/channel GUID, link, or username."
            )

        if request_needed is not None and not isinstance(request_needed, bool):
            raise InvalidInput("'request_needed' must be of boolean type only.")

        join_link = join_link.split("/")[-1]

        update_parameters = []
        input_data = {
            'object_guid': chat_guid,
            'join_link': join_link,
        }

        if expire_time is not None:
            input_data['expire_time'] = expire_time
            update_parameters.append('expire_time')

        if request_needed is not None:
            input_data['request_needed'] = request_needed
            update_parameters.append('request_needed')

        if title is not None:
            input_data['title'] = title
            update_parameters.append('title')

        if usage_limit is not None:
            input_data['usage_limit'] = usage_limit
            update_parameters.append('usage_limit')

        if not update_parameters:
            raise InvalidInput(
                "At least one of 'expire_time', 'request_needed', "
                "'title', or 'usage_limit' must be provided."
            )

        input_data['update_parameters'] = update_parameters

        return await self.request(method = 'editJoinLink', input = input_data)