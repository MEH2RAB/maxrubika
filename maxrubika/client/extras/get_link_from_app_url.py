from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetLinkFromAppUrl:
    async def get_link_from_app_url(
        self: "maxrubika.Messenger",
        url: str
    ):
        """
        Get a direct link from an application URL.

        Parameters:
            url (str): The application URL to extract the link from.

        Returns:
            The result containing the extracted link.
        """
        return await self.request(
            method='getLinkFromAppUrl',
            input={'app_url': url}
        )