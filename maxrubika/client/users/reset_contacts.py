import maxrubika

class ResetContacts:
    async def reset_contacts(self: "maxrubika.Client"):
        """
        Reset all saved contacts for the authenticated user.

        This method clears the entire contact list on the server side.

        Returns:
            The result of the API call.
        """
        return await self.request(method = 'resetContacts')