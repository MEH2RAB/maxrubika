from typing import List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetContactsLastOnline:
    async def get_contacts_last_online(
        self: "maxrubika.Messenger",
        users: Union[str, List[str]]
    ):
        """
        Get the last online status of multiple users.

        Parameters:
            users (Union[str, List[str]]): The GUID(s) or username(s) of the contacts.

        Returns:
            Last online status for each user.
        """
        from ..exceptions import InvalidInput

        if isinstance(users, str):
            users = [users]

        user_guids = []

        for user in users:
            guid = await self.get_guid(user)

            if not guid.startswith("u0"):
                message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
                raise InvalidInput(message)

            user_guids.append(guid)

        return await self.request(method='getContactsLastOnline', input={'user_guids': user_guids})