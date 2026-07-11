import re
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
        rubika_link_regex = r'^https:\/\/rubika\.ir\/(?:joinc|joing)\/?\+?([A-Z]{8}0[A-Z]{23}|[A-Z]{9}0[A-Z]{22})$'

        if re.match(rubika_link_regex, link, re.IGNORECASE):
            hash_link = link.split('/')[-1]
            link_lower = link.lower()

            if link_lower.startswith('https://rubika.ir/joinc/'):
                return await self.request(
                    method = 'channelPreviewByJoinLink',
                    input = {'hash_link': hash_link}
                )
            elif link_lower.startswith('https://rubika.ir/joing/'):
                return await self.request(
                    method = 'groupPreviewByJoinLink',
                    input = {'hash_link': hash_link}
                )
        else:
            message = "Invalid Rubika link format. Links must start with 'https://rubika.ir/joing/' or 'https://rubika.ir/joinc/' and follow the specified hash format."
            raise InvalidInput(message)