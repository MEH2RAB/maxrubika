import maxrubika
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
        group_lower = group.lower()

        if group_lower.startswith('https://rubika.ir/joing/'):
            hash_link = group.rstrip('/').split('/')[-1].split('?')[0].split('#')[0]
            return await self.request(
                method = 'joinGroup',
                input = {'hash_link': hash_link}
            )
        else:
            message = "'link' must start with 'https://rubika.ir/joing/' and follow the specified hash format."
            raise InvalidInput(message)