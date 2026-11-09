from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMyCloseFriends:
    async def get_my_close_friends(
        self: "maxrubika.Rubino",
        search_text: Optional[str] = None,
        limit: Optional[int] = None,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get the list of close friends.

        Parameters:
            search_text (str, optional): Search text for filtering close friends. Defaults to None.
            limit (int, optional): The maximum number of close friends to return. Defaults to None (server default).
            start_id (str, optional): The starting profile ID for pagination. Defaults to None.
            my_profile (str, optional): The profile to query. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {'profile_id': profile_id}

        if search_text is not None:
            input_data['search_text'] = search_text

        if limit is not None:
            input_data['limit'] = limit

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getMyCloseFriends',
            input=input_data
        )