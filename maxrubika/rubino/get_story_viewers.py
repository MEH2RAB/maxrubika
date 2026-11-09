from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetStoryViewers:
    async def get_story_viewers(
        self: "maxrubika.Rubino",
        story_id: str,
        start_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Get the viewers of a story.

        Parameters:
            story_id (str): The ID of the story.
            start_id (str, optional): The starting viewer ID for pagination. Defaults to None.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'story_id': story_id
        }

        if start_id is not None:
            input_data['start_id'] = start_id

        return await self.request(
            method='getStoryViewers',
            input=input_data
        )