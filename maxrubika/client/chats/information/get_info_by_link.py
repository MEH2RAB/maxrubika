from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetInfoByLink:
    async def get_info_by_link(
        self: "maxrubika.Messenger",
        link: str
    ):
        """
        Get group or channel preview by join link.

        Parameters:
            link (str): The join link.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        link_lower = link.lower()

        hash_link = link.rstrip('/').split('/')[-1].split('?')[0].split('#')[0]

        if link_lower.startswith(('https://rubika.ir/joinc/', 'https://shad.ir/joinc/')):
            return await self.request(
                method='channelPreviewByJoinLink',
                input={'hash_link': hash_link}
            )

        if link_lower.startswith(('https://rubika.ir/joing/', 'https://shad.ir/joing/')):
            return await self.request(
                method='groupPreviewByJoinLink',
                input={'hash_link': hash_link}
            )

        message = (
            "Invalid link format. Links must start with "
            "'https://rubika.ir/joing/', 'https://rubika.ir/joinc/', "
            "'https://shad.ir/joing/', or 'https://shad.ir/joinc/' "
            "and follow the specified hash format."
        )
        raise InvalidInput(message)