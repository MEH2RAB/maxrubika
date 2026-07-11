from typing import Union, List, Optional
import maxrubika
from ..exceptions import InvalidInput

class CreateGroup:
    async def create_group(
        self: "maxrubika.Client",
        title: str,
        members: Union[str, List[str]],
        description: Optional[str] = None
    ):
        """
        Create a new group.

        Parameters:
            title (str): The title of the group.
            members (Union[str, List[str]]): A single member GUID/Username or a list of member GUIDs/Usernames to be added to the group.
            description (Optional[str]): Description of the group (optional). Defaults to None.

        Returns:
            The result of the API call.
        """
        if isinstance(members, str):
            members = [members]

        if not members:
            raise InvalidInput("At least one member is required to create a group.")

        if len(title) > 60:
            raise InvalidInput("Title cannot exceed 60 characters.")
        if len(title) == 0:
            raise InvalidInput("Title cannot be empty.")

        if description is not None:
            if len(description) > 300:
                raise InvalidInput("Description cannot exceed 300 characters.")

        member_guids = []

        for member in members:
            guid = await self.get_guid(member)

            if not guid.startswith(("u0", "b0")):
                message = f"'{member}' does not point to a valid member. Expected a user GUID, bot GUID, or username."
                raise InvalidInput(message)

            member_guids.append(guid)

        return await self.request(
            method = 'addGroup',
            input = {
                'title': title.strip(),
                'member_guids': member_guids,
                'description': description
            }
        )