from typing import Optional, Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetProfileStories:
    async def get_profile_stories(
        self: "maxrubika.Rubino",
        target_profile: str,
        story_ids: Optional[Union[str, List[str]]] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get stories of a profile.

        Parameters:
            target_profile (str): The profile ID or username that owns the stories.
            story_ids (Union[str, List[str]], optional): A single story ID or a list of story IDs to fetch specific stories. If not provided, all stories are returned. Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The stories data.
        """
        from .exceptions import InvalidInput

        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'target_profile_id': target_profile_id
        }

        if story_ids is not None:
            if isinstance(story_ids, str):
                story_ids = [story_ids]

            if not isinstance(story_ids, list):
                message = "'story_ids' must be a string or list."
                raise InvalidInput(message)

            unique_story_ids = []
            for sid in story_ids:
                if sid not in unique_story_ids:
                    unique_story_ids.append(sid)

            input_data['story_ids'] = unique_story_ids

        return await self.request(
            method='getStories',
            input=input_data
        )