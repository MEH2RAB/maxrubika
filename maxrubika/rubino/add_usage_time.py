from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AddUsageTime:
    async def add_usage_time(
        self: "maxrubika.Rubino",
        usage_time_list: List[Dict[str, Any]],
        my_profile: Optional[str] = None
    ):
        """
        Register usage time analytics.

        Parameters:
            usage_time_list (List[Dict[str, Any]]): List of usage time entries. Each entry must contain 'page' (exactly one of 'Feed', 'Profile', 'Story', 'Live', 'Explore', 'Search' — case-sensitive) and 'duration' (any value). Optional 'extra_data' may contain 'post_data_id' (dict with 'post_id' and 'post_profile_id'), 'profile_id' (str), and 'live_id' (str).
            my_profile (str, optional): The profile that reports usage. Defaults to self.profile_id.

        Returns:
            The response data.

        Examples:
            # Single page usage
            await client.add_usage_time(
                usage_time_list=[
                    {"page": "Feed", "duration": 3000}
                ],
                my_profile="MAXRubikaTest"
            )

            # Feed with post data
            await client.add_usage_time(
                usage_time_list=[
                    {
                        "page": "Feed",
                        "duration": 3000,
                        "extra_data": {
                            "post_data_id": {
                                "post_id": "6aee295d805bf66cedd0c202",
                                "post_profile_id": "6a807217b59333f89d394d36"
                            }
                        }
                    }
                ],
                my_profile="MAXRubikaTest"
            )

            # Profile view
            await client.add_usage_time(
                usage_time_list=[
                    {
                        "page": "Profile",
                        "duration": 10000,
                        "extra_data": {"profile_id": "6a807217b59333f89d394d36"}
                    }
                ],
                my_profile="MAXRubikaTest"
            )

            # Live view
            await client.add_usage_time(
                usage_time_list=[
                    {
                        "page": "Live",
                        "duration": 20000,
                        "extra_data": {"live_id": "live_123"}
                    }
                ],
                my_profile="MAXRubikaTest"
            )

            # Multiple entries
            await client.add_usage_time(
                usage_time_list=[
                    {"page": "Feed", "duration": 3000},
                    {"page": "Explore", "duration": 8000},
                    {"page": "Search", "duration": 4000}
                ],
                my_profile="MAXRubikaTest"
            )
        """
        from .exceptions import InvalidInput

        valid_pages = {'Feed', 'Profile', 'Story', 'Live', 'Explore', 'Search'}

        if not isinstance(usage_time_list, list):
            message = "'usage_time_list' must be a list."
            raise InvalidInput(message)

        for item in usage_time_list:
            if not isinstance(item, dict):
                message = "Each usage time entry must be a dict."
                raise InvalidInput(message)

            page = item.get('page')
            if page not in valid_pages:
                message = "Each entry's 'page' must be exactly one of: 'Feed', 'Profile', 'Story', 'Live', 'Explore', 'Search' (case-sensitive)."
                raise InvalidInput(message)

            if 'duration' not in item:
                message = "Each entry must contain 'duration'."
                raise InvalidInput(message)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'usage_time_list': usage_time_list
        }

        return await self.request(
            method='addUsageTime',
            input=input_data
        )