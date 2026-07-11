import maxrubika

class SeenChats:
    async def seen_chats(self: "maxrubika.Client", seen_list: dict):
        """
        Marks multiple chats as seen.

        Parameters:
            seen_list (dict): A dictionary containing chat GUIDs and their last seen message IDs.

        Returns:
            The result of the operation.
        """
        return await self.request(method = 'seenChats', input = {'seen_list': seen_list})