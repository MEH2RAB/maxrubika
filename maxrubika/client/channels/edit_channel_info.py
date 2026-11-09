from typing import Optional, Literal, Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class EditChannelInfo:
    async def edit_channel_info(
        self: "maxrubika.Messenger",
        channel: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        username: Optional[str] = None,
        channel_type: Optional[Literal['Public', 'Private']] = None,
        sign_messages: Optional[bool] = None,
        is_restricted_content: Optional[bool] = None,
        reactions: Optional[Union[Literal['All', 'Disable'], List[int]]] = None
    ):
        """
        Edit information of a channel.

        Parameters:
            channel (str): The GUID, link, or username of the channel.
            title (str, optional): The new title. Max 60 characters.
            description (str, optional): The new description. Max 300 characters.
            username (str, optional): The new username. Max 32 characters.
            channel_type (str, optional): 'Public' or 'Private'. Case-insensitive.
            sign_messages (bool, optional): Whether to sign messages in the channel.
            is_restricted_content (bool, optional): Restrict content (prevent screenshots and file saving).
            reactions (Union[Literal['All', 'Disable'], List[int]], optional): 'All', 'Disable', or a list of reaction IDs.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

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
        input_data = {'channel_guid': channel_guid}

        if title is not None:
            input_data['title'] = title
            updated_parameters.append('title')

        if description is not None:
            input_data['description'] = description
            updated_parameters.append('description')

        if username is not None:
            await self.update_channel_username(channel_guid, username)

        if channel_type is not None:
            channel_type_map = {
                'public': 'Public',
                'private': 'Private'
            }

            normalized_channel_type = channel_type_map.get(str(channel_type).lower())

            if not normalized_channel_type:
                raise InvalidInput("'channel_type' must be either 'Public' or 'Private'.")

            input_data['channel_type'] = normalized_channel_type
            updated_parameters.append('channel_type')

        if sign_messages is not None:
            input_data['sign_messages'] = sign_messages
            updated_parameters.append('sign_messages')

        if is_restricted_content is not None:
            input_data['is_restricted_content'] = is_restricted_content
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
                raise InvalidInput("'reactions' must be 'All', 'Disable', or a list of reaction IDs.")

            input_data['chat_reaction_setting'] = reaction_dict
            updated_parameters.append('chat_reaction_setting')

        input_data['updated_parameters'] = updated_parameters
        return await self.request(method='editChannelInfo', input=input_data)