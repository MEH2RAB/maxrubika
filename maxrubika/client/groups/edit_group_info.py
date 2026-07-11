from typing import Optional, Union, Dict, List, Literal
import maxrubika
from ..exceptions import InvalidInput

class EditGroupInfo:
    async def edit_group_info(
        self: "maxrubika.Client",
        group: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        slow_mode: Optional[str] = None,
        event_messages: Optional[bool] = None,
        is_restricted_content: Optional[bool] = None,
        reactions: Optional[Union[Literal['All', 'Disable'], List[int]]] = None,
        chat_history_for_new_members: Optional[str] = None,
        restricted_period: Optional[List[Dict[str, Union[List[str], str]]]] = None
    ):
        """
        Edit the information of a group.

        Parameters:
            group (str): The GUID or link of the group.
            title (Optional[str]): The new title for the group (max 60 characters).
            description (Optional[str]): The new description for the group (max 300 characters).
            slow_mode (Optional[str]): The new slow mode setting for the group.
            event_messages (Optional[bool]): Enable or disable event messages for the group.
            is_restricted_content (Optional[bool]): Restrict content (prevent screenshots and file saving).
            reactions (Union[Literal['All', 'Disable'], List[int]], optional): 
                - 'All': Enable all reactions
                - 'Disable': Disable all reactions
                - List[int]: List of reaction IDs to enable (e.g., [1, 2, 6, 7, 8, 23, 44])
            chat_history_for_new_members (Optional[str]): The new chat history setting for new members.
            restricted_period (Optional[List[Dict[str, Union[List[str], str]]]]): 
                Time restrictions for sending messages (list of periods). Each period should contain:
                - days_of_week: List of days ['Saturday', 'Sunday', ..., 'Friday']
                - from_time: Start time in "HH:MM" format (24-hour)
                - to_time: End time in "HH:MM" format (24-hour)
                Note: Can accept multiple periods as a list of dictionaries.

        Returns:
            The result of the API call.

        Examples:
            # Enable all reactions
            await client.edit_group_info(
                group="g0...",
                reactions="All"
            )

            # Disable all reactions
            await client.edit_group_info(
                group="g0...",
                reactions="Disable"
            )

            # Enable specific reactions
            await client.edit_group_info(
                group="g0...",
                reactions=[1, 2, 6, 7, 8, 23, 44]
            )

            # Single restricted period
            await client.edit_group_info(
                group="g0...",
                restricted_period=[{
                    "days_of_week": ["Saturday", "Sunday"],
                    "from_time": "00:00",
                    "to_time": "06:00"
                }]
            )

            # Multiple restricted periods
            await client.edit_group_info(
                group="g0...",
                restricted_period=[
                    {
                        "days_of_week": ["Saturday", "Sunday", "Monday"],
                        "from_time": "01:13",
                        "to_time": "08:16"
                    },
                    {
                        "days_of_week": ["Tuesday", "Wednesday"],
                        "from_time": "22:00",
                        "to_time": "04:00"  # Can cross midnight
                    }
                ]
            )
        """
        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        updated_parameters = []
        input_data = {'group_guid': group_guid}

        if title is not None:
            if len(title) > 60:
                raise InvalidInput("Title cannot exceed 60 characters.")
            input_data['title'] = title
            updated_parameters.append('title')

        if description is not None:
            if len(description) > 300:
                raise InvalidInput("Description cannot exceed 300 characters.")
            input_data['description'] = description
            updated_parameters.append('description')

        if slow_mode is not None:
            input_data['slow_mode'] = slow_mode
            updated_parameters.append('slow_mode')

        if event_messages is not None:
            input_data['event_messages'] = event_messages
            updated_parameters.append('event_messages')

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

            input_data['chat_reaction_setting'] = reaction_dict
            updated_parameters.append('chat_reaction_setting')

        if is_restricted_content is not None:
            input_data['is_restricted_content'] = is_restricted_content
            updated_parameters.append('is_restricted_content')

        if chat_history_for_new_members is not None:
            if chat_history_for_new_members not in ('Hidden', 'Visible'):
                message = "'chat_history_for_new_members' argument can only be in 'Hidden' or 'Visible'."
                raise InvalidInput(message)

            input_data['chat_history_for_new_members'] = chat_history_for_new_members
            updated_parameters.append('chat_history_for_new_members')

        if restricted_period is not None:
            self._validate_restricted_periods(restricted_period)
            input_data['restricted_message_sending_period'] = restricted_period
            updated_parameters.append('restricted_message_sending_period')

        input_data['updated_parameters'] = updated_parameters
        return await self.request(method='editGroupInfo', input=input_data)

    def _validate_restricted_periods(self, periods: List[Dict[str, Union[List[str], str]]]) -> None:
        valid_days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        if not isinstance(periods, list):
            raise InvalidInput("'restricted_period' must be a list.")

        for period in periods:
            if not isinstance(period, dict):
                raise InvalidInput("Each period must be a dictionary.")

            if 'days_of_week' not in period:
                raise InvalidInput("Each period must have 'days_of_week' key.")

            days = period['days_of_week']
            if not isinstance(days, list):
                raise InvalidInput("'days_of_week' must be a list.")

            if not days:
                raise InvalidInput("'days_of_week' cannot be empty.")

            for day in days:
                if day not in valid_days:
                    message = f"Invalid day: {day}. Valid days are: {valid_days}"
                    raise InvalidInput(message)

            for time_key in ['from_time', 'to_time']:
                if time_key not in period:
                    message = f"Each period must have '{time_key}' key."
                    raise InvalidInput(message)

                time_str = period[time_key]
                if not isinstance(time_str, str):
                    raise InvalidInput(f"{time_key} must be a string.")

                try:
                    hours, minutes = map(int, time_str.split(':'))
                    if not (0 <= hours <= 23) or not (0 <= minutes <= 59):
                        raise InvalidInput()
                    if len(time_str) != 5 or time_str[2] != ':':
                        raise InvalidInput()
                except (ValueError, IndexError):
                    message = f"{time_key} must be in 'HH:MM' format (24-hour)."
                    raise InvalidInput(message)