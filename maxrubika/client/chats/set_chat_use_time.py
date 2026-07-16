import maxrubika

class SetChatUseTime:
    async def set_chat_use_time(
        self: "maxrubika.Client",
        chat: str,
        use_time: int
    ):
        """
        Send chat usage time to the server.

        This helps the server recognize natural user behavior
        and can reduce rate limiting and bot detection.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            use_time (int): Time spent in the chat in milliseconds.

        Returns:
            The result of the API call.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'setChatUseTime',
            input = {
                'object_guid': chat_guid,
                'time': use_time
            }
        )