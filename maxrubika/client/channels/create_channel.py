from typing import Union
import maxrubika
from ..exceptions import InvalidInput

class CreateChannel:
    async def create_channel(
        self: "maxrubika.Client",
        title: str,
        members: Union[str, list] = None,
        channel_type: str = 'Public',
        description: str = None
    ):
        """
        Create a new channel.

        Parameters:
            title (str): The title of the new channel.
            members (Union[str, list], optional): The GUID(s) or username(s) of the member(s) to be added to the new channel. Default is None.
            channel_type (str): Set type of the channel. 'Public' or 'Private'. Default is 'Public'.
            description (str, optional): The description of the new channel. Default is None.

        Returns:
            The result of the API call.
        """
        if channel_type not in ('Public', 'Private'):
            raise InvalidInput("'channel_type' must be either 'Public' or 'Private'.")

        if len(title) > 60:
            raise InvalidInput("Title cannot exceed 60 characters.")
        if len(title) == 0:
            raise InvalidInput("Title cannot be empty.")

        if description is not None:
            if len(description) > 300:
                raise InvalidInput("Description cannot exceed 300 characters.")

        input_data = {'title': title, 'description': description, 'channel_type': channel_type}

        member_guids = []
        if members is not None:
            if isinstance(members, str):
                members = [members]

            for member in members:
                guid = await self.get_guid(member)

                if not guid.startswith(("u0", "b0")):
                    message = f"'{member}' does not point to a valid member. Expected a user GUID, bot GUID, or username."
                    raise InvalidInput(message)

                member_guids.append(guid)

            input_data['member_guids'] = member_guids

        return await self.request(method = 'addChannel', input = input_data)