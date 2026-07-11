import re; import maxrubika
from ..exceptions import InvalidInput

class JoinGroup:
    async def join_group(self: "maxrubika.Client", group: str):
        """
        Join a group using the provided link.

        Parameters:
            group (str): The group link.

        Returns:
            The result of the API call.
        """
        group_link_regex = r'^https:\/\/rubika\.ir\/(?:joing)\/?\+?([A-Z]{8}0[A-Z]{23}|[A-Z]{9}0[A-Z]{22})$'

        if re.match(group_link_regex, group):
            hash_link = group.split('/')[-1]

        else:
            message = "'link' must start with 'https://rubika.ir/going' and follow the specified hash format."
            raise InvalidInput(message)

        return await self.request(method = 'joinGroup', input = {'hash_link': hash_link})