from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetContactsStories:
    async def get_contacts_stories(self: "maxrubika.Messenger"):
        """
        Get stories from contacts in the chat page.

        Returns:
            The result of the API call containing contacts stories.
        """
        return await self.request(method='getStories')