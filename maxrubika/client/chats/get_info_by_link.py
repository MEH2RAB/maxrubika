import maxrubika
from ..exceptions import InvalidInput

class GetInfoByLink:
    async def get_info_by_link(self: "maxrubika.Client", link: str):
        """
        Get group or channel preview by join link.

        Parameters:
            link (str): The join link.

        Returns:
            The result of the API call.
        """
        link_lower = link.lower()
        
        if link_lower.startswith('https://rubika.ir/joinc/'):
            hash_link = link.rstrip('/').split('/')[-1].split('?')[0].split('#')[0]
            return await self.request(
                method = 'channelPreviewByJoinLink',
                input = {'hash_link': hash_link}
            )
        elif link_lower.startswith('https://rubika.ir/joing/'):
            hash_link = link.rstrip('/').split('/')[-1].split('?')[0].split('#')[0]
            return await self.request(
                method = 'groupPreviewByJoinLink',
                input = {'hash_link': hash_link}
            )
        else:
            message = "Invalid Rubika link format. Links must start with 'https://rubika.ir/joing/' or 'https://rubika.ir/joinc/' and follow the specified hash format."
            raise InvalidInput(message)