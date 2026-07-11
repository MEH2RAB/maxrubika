import maxrubika

class GetProfileLinkItems:
    async def get_profile_link_items(self: "maxrubika.Client", chat: str):
        """
        Get profile link items for a given chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(method = 'getProfileLinkItems', input = {'object_guid': chat_guid})