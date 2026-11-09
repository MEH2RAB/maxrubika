from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DeleteStory:
    async def delete_story(
        self: "maxrubika.Rubino",
        story_id: str,
        my_profile: Optional[str] = None
    ):
        """
        Delete a story.

        Parameters:
            story_id (str): The ID of the story to delete.
            my_profile (str, optional): The profile that deletes. Defaults to self.profile_id.

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

        return await self.request(
            method='deleteStory',
            input=input_data
        )