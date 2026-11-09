from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetEvents:
    async def get_events(
        self: "maxrubika.Rubino",
        filter: Optional[Literal['FollowRequest', 'PostConfirm', 'ProfileConfirm']] = None,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get profile events.

        Parameters:
            filter (Literal['FollowRequest', 'PostConfirm', 'ProfileConfirm'], optional): The event filter. Case-insensitive. Defaults to None (all events).
            start_id (str, optional): The starting event ID for pagination. Defaults to None.
            my_profile (str, optional): The profile to query. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        filter_map = {
            'followrequest': 'FollowRequest',
            'postconfirm': 'PostConfirm',
            'profileconfirm': 'ProfileConfirm'
        }

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {'profile_id': profile_id}

        if filter is not None:
            normalized_filter = filter_map.get(filter.lower()) if isinstance(filter, str) else None
            if not normalized_filter:
                message = "'filter' must be 'FollowRequest', 'PostConfirm', or 'ProfileConfirm'."
                raise InvalidInput(message)
            input_data['filter'] = normalized_filter

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getEvents',
            input=input_data
        )