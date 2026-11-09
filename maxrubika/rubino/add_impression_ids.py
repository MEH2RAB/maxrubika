from typing import List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class AddImpressionIDs:
    async def add_impression_ids(
        self: "maxrubika.Rubino",
        impression_data_list: List[Dict],
        my_profile: Optional[str] = None
    ):
        """
        Register impressions for posts or profiles to improve content recommendations.

        Parameters:
            impression_data_list (List[Dict]): List of impression data objects. Each item must contain 'type' ('Post' or 'Profile'); 'track_id' is optional. For 'Post' type, provide 'post_data_id' as a dict with 'post_id' and 'post_profile_id'. For 'Profile' type, provide 'profile_id'.
            my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

        Returns:
            The response data.

        Examples:
            # Register a profile impression
            await client.add_impression_ids(
                impression_data_list=[
                    {
                        "type": "Profile",
                        "profile_id": "6a8819ce04fe81a4c8af4455"
                    }
                ],
                my_profile="MAXRubikaTest"
            )

            # Register a post impression
            await client.add_impression_ids(
                impression_data_list=[
                    {
                        "type": "Post",
                        "post_data_id": {
                            "post_id": "6ae61abdfc4eff521f9f0448",
                            "post_profile_id": "6a8819ce04fe81a4c8af4455"
                        }
                    }
                ],
                my_profile="MAXRubikaTest"
            )
        """
        from .exceptions import InvalidInput

        if self.api_version == 0:
            raise InvalidInput("This method is not supported in API version 0.")

        if not isinstance(impression_data_list, list) or not impression_data_list:
            raise InvalidInput("'impression_data_list' must be a non-empty list.")

        normalized_list = []

        for item in impression_data_list:
            if not isinstance(item, dict):
                raise InvalidInput("Each impression item must be a dict.")

            item_type = item.get('type')

            if not isinstance(item_type, str):
                raise InvalidInput("Each impression item must have a 'type' ('Post' or 'Profile').")

            item_type = item_type.lower()
            track_id = item.get('track_id')

            if item_type == 'post':
                post_data_id = item.get('post_data_id')
                if not isinstance(post_data_id, dict):
                    raise InvalidInput("'Post' impression item must have a 'post_data_id' dict.")
                if not post_data_id.get('post_id') or not post_data_id.get('post_profile_id'):
                    raise InvalidInput("'post_data_id' must contain 'post_id' and 'post_profile_id'.")

                normalized_item = {
                    'type': 'Post',
                    'post_data_id': {
                        'post_id': post_data_id['post_id'],
                        'post_profile_id': post_data_id['post_profile_id']
                    }
                }
            elif item_type == 'profile':
                profile_id = item.get('profile_id')
                if not isinstance(profile_id, str) or not profile_id:
                    raise InvalidInput("'Profile' impression item must have a 'profile_id' string.")

                normalized_item = {
                    'type': 'Profile',
                    'profile_id': profile_id
                }
            else:
                raise InvalidInput("'type' must be 'Post' or 'Profile'.")

            if track_id is not None:
                if not isinstance(track_id, str):
                    raise InvalidInput("'track_id' must be a string.")
                normalized_item['track_id'] = track_id

            normalized_list.append(normalized_item)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'impression_data_list': normalized_list
        }

        return await self.request(
            method='addImpressionIds',
            input=input_data
        )