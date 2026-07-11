from typing import Optional, Literal, Union, List
import maxrubika
from ..exceptions import InvalidInput

class EditChannelInfo:
    async def edit_channel_info(
        self: "maxrubika.Client",
        channel: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        username: Optional[str] = None,
        channel_type: Literal['Public', 'Private'] = None,
        sign_messages: Optional[bool] = None,
        is_restricted_content: Optional[bool] = None,
        reactions: Optional[Union[Literal['All', 'Disable'], List[int]]] = None
    ):
        """
        Edit information of a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            title (str, optional): The new title of the channel. Max 60 characters.
            description (str, optional): The new description of the channel. Max 300 characters.
            username (str, optional): The new username of the channel. Max 32 characters.
            channel_type (str, optional): The new type of the channel. 'Public' or 'Private'.
            sign_messages (bool, optional): Whether to sign messages in the channel.
            is_restricted_content (bool, optional): Restrict content (prevent screenshots and file saving).
            reactions (Union[Literal['All', 'Disable'], List[int]], optional): 
                - 'All': Enable all reactions
                - 'Disable': Disable all reactions
                - List[int]: List of reaction IDs to enable (e.g., [1, 2, 6, 7, 8, 23, 44])

        Returns:
            The result of the API call.
        """
        if title is not None:
            if len(title) > 60:
                raise InvalidInput("Title cannot exceed 60 characters.")
            if len(title) == 0:
                raise InvalidInput("Title cannot be empty.")

        if description is not None:
            if len(description) > 300:
                raise InvalidInput("Description cannot exceed 300 characters.")

        channel_guid = await self.get_guid(channel)

        if not channel_guid.startswith("c0"):
            message = f"'{channel}' does not point to a valid channel. Expected a channel GUID, channel link, or channel username."
            raise InvalidInput(message)

        updated_parameters = []
        input = {'channel_guid': channel_guid}

        if title is not None:
            input['title'] = title
            updated_parameters.append('title')

        if description is not None:
            input['description'] = description
            updated_parameters.append('description')

        if username is not None:
            await self.update_channel_username(channel_guid, username)

        if channel_type is not None:
            if channel_type not in ('Public', 'Private'):
                message = "'channel_type' argument can only be in 'Public' or 'Private'."
                raise InvalidInput(message)

            input['channel_type'] = channel_type
            updated_parameters.append('channel_type')

        if sign_messages is not None:
            input['sign_messages'] = sign_messages
            updated_parameters.append('sign_messages')

        if is_restricted_content is not None:
            input['is_restricted_content'] = is_restricted_content
            updated_parameters.append('is_restricted_content')

        if reactions is not None:
            reaction_dict = {}
            
            if reactions == "All":
                reaction_dict["reaction_type"] = "All"
            elif reactions == "Disable":
                reaction_dict["reaction_type"] = "Disabled"
            elif isinstance(reactions, list):
                reaction_dict["reaction_type"] = "Selected"
                reaction_dict["selected_reactions"] = reactions
            else:
                raise InvalidInput(
                    "'reactions' must be 'All', 'Disable', or a list of reaction IDs."
                )

            input['chat_reaction_setting'] = reaction_dict
            updated_parameters.append('chat_reaction_setting')

        input['updated_parameters'] = updated_parameters
        return await self.request(method = 'editChannelInfo', input = input)