from typing import TYPE_CHECKING, Optional, Union, Dict, List, Literal

if TYPE_CHECKING:
    import maxrubika

class EditGroupInfo:
    async def edit_group_info(
        self: "maxrubika.Messenger",
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
            title (str, optional): The new title for the group (max 60 characters).
            description (str, optional): The new description for the group (max 300 characters).
            slow_mode (str, optional): The new slow mode setting for the group.
            event_messages (bool, optional): Enable or disable event messages for the group.
            is_restricted_content (bool, optional): Restrict content (prevent screenshots and file saving).
            reactions (Union[Literal['All', 'Disable'], List[int]], optional): 'All' to enable all reactions, 'Disable' to disable all, or a list of reaction IDs to enable (e.g., [1, 2, 6, 7, 8, 23, 44]). Case-insensitive.
            chat_history_for_new_members (str, optional): The new chat history setting for new members ('Hidden' or 'Visible'). Case-insensitive.
            restricted_period (List[Dict[str, Union[List[str], str]]], optional): Time restrictions for sending messages (list of periods). Each period should contain days_of_week (list of days ['Saturday', 'Sunday', ..., 'Friday'], case-insensitive), from_time (start time in "HH:MM" format, 24-hour), and to_time (end time in "HH:MM" format, 24-hour). Can accept multiple periods as a list of dictionaries.

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
        from ..exceptions import InvalidInput

        group_guid = await self.get_guid(group)

        if not group_guid.startswith("g0"):
            message = f"'{group}' does not point to a valid group. Expected a group GUID or group link."
            raise InvalidInput(message)

        updated_parameters = []
        input_data = {'group_guid': group_guid}

        if title is not None:
            if len(title) > 60:
                message = "Title cannot exceed 60 characters."
                raise InvalidInput(message)
            input_data['title'] = title
            updated_parameters.append('title')

        if description is not None:
            if len(description) > 300:
                message = "Description cannot exceed 300 characters."
                raise InvalidInput(message)
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

            if isinstance(reactions, str):
                normalized = reactions.lower()
                if normalized == "all":
                    reaction_dict["reaction_type"] = "All"
                elif normalized == "disable":
                    reaction_dict["reaction_type"] = "Disabled"
                else:
                    message = "'reactions' must be 'All', 'Disable', or a list of reaction IDs."
                    raise InvalidInput(message)
            elif isinstance(reactions, list):
                reaction_dict["reaction_type"] = "Selected"
                reaction_dict["selected_reactions"] = reactions
            else:
                message = "'reactions' must be 'All', 'Disable', or a list of reaction IDs."
                raise InvalidInput(message)

            input_data['chat_reaction_setting'] = reaction_dict
            updated_parameters.append('chat_reaction_setting')

        if is_restricted_content is not None:
            input_data['is_restricted_content'] = is_restricted_content
            updated_parameters.append('is_restricted_content')

        if chat_history_for_new_members is not None:
            history_map = {
                'hidden': 'Hidden',
                'visible': 'Visible'
            }
            chat_history_for_new_members = history_map.get(chat_history_for_new_members.lower())

            if not chat_history_for_new_members:
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
        from ..exceptions import InvalidInput

        valid_days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        days_map = {day.lower(): day for day in valid_days}

        if not isinstance(periods, list):
            message = "'restricted_period' must be a list."
            raise InvalidInput(message)

        for period in periods:
            if not isinstance(period, dict):
                message = "Each period must be a dictionary."
                raise InvalidInput(message)

            if 'days_of_week' not in period:
                message = "Each period must have 'days_of_week' key."
                raise InvalidInput(message)

            days = period['days_of_week']
            if not isinstance(days, list):
                message = "'days_of_week' must be a list."
                raise InvalidInput(message)

            if not days:
                message = "'days_of_week' cannot be empty."
                raise InvalidInput(message)

            normalized_days = []
            for day in days:
                if not isinstance(day, str):
                    message = f"Invalid day: {day}. Valid days are: {valid_days}"
                    raise InvalidInput(message)

                normalized_day = days_map.get(day.lower())
                if not normalized_day:
                    message = f"Invalid day: {day}. Valid days are: {valid_days}"
                    raise InvalidInput(message)

                normalized_days.append(normalized_day)

            period['days_of_week'] = normalized_days

            for time_key in ['from_time', 'to_time']:
                if time_key not in period:
                    message = f"Each period must have '{time_key}' key."
                    raise InvalidInput(message)

                time_str = period[time_key]
                if not isinstance(time_str, str):
                    message = f"{time_key} must be a string."
                    raise InvalidInput(message)

                try:
                    hours, minutes = map(int, time_str.split(':'))
                    valid = (0 <= hours <= 23) and (0 <= minutes <= 59) and len(time_str) == 5 and time_str[2] == ':'
                except (ValueError, IndexError):
                    valid = False

                if not valid:
                    message = f"{time_key} must be in 'HH:MM' format (24-hour)."
                    raise InvalidInput(message) from None