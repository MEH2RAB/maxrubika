from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SearchProfile:
    async def search_profile(
        self: "maxrubika.Rubino",
        search_text: str,
        usage: Literal['Search', 'AddCloseFriend', 'AddTag', 'AddCollaborator', 'AddMention', 'AddBrandPartner', 'AddAdmin', 'MessageReceiver'] = 'Search',
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Search for profiles.

        Parameters:
            search_text (str): The search text (username or name).
            usage (Literal['Search', 'AddCloseFriend', 'AddTag', 'AddCollaborator', 'AddMention', 'AddBrandPartner', 'AddAdmin', 'MessageReceiver']): The search usage context. Case-insensitive. Default is 'Search'.
            start_id (str, optional): The starting profile ID for pagination. Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        usage_map = {
            'search': 'Search',
            'addclosefriend': 'AddCloseFriend',
            'addtag': 'AddTag',
            'addcollaborator': 'AddCollaborator',
            'addmention': 'AddMention',
            'addbrandpartner': 'AddBrandPartner',
            'addadmin': 'AddAdmin',
            'messagereceiver': 'MessageReceiver'
        }

        normalized_usage = usage_map.get(usage.lower()) if isinstance(usage, str) else None
        if not normalized_usage:
            message = "'usage' must be 'Search', 'AddCloseFriend', 'AddTag', 'AddCollaborator', 'AddMention', 'AddBrandPartner', 'AddAdmin', or 'MessageReceiver'."
            raise InvalidInput(message)

        if not search_text or not search_text.strip():
            message = "'search_text' must be a non-empty string."
            raise InvalidInput(message)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'search_text': search_text.replace('@', ''),
            'usage': normalized_usage
        }

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='searchProfile',
            input=input_data
        )