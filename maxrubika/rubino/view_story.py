from typing import Optional, Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ViewStory:
    async def view_story(
        self: "maxrubika.Rubino",
        target_profile: str,
        story_id: Union[str, List[str]],
        my_profile: Optional[str] = None
    ):
        """
        Mark stories as viewed.

        Parameters:
            target_profile (str): The profile ID or username that owns the stories.
            story_id (str | list): A story ID or list of story IDs.
            my_profile (str, optional): The profile that views. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if isinstance(story_id, str):
            story_id = [story_id]

        unique_story_ids = []
        for sid in story_id:
            if sid not in unique_story_ids:
                unique_story_ids.append(sid)

        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'story_profile_id': target_profile_id,
            'story_ids': unique_story_ids
        }

        return await self.request(
            method='addViewStory',
            input=input_data
        )