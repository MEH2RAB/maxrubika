import maxrubika

class GetLinkFromAppUrl:
    async def get_link_from_app_url(
        self: "maxrubika.Client",
        url: str
    ):
        """
        Get a direct link from an application URL.

        Parameters:
            url (str): The application URL to extract the link from.

        Returns:
            Data: The result containing the extracted link.
        """
        return await self.request(
            method = 'getLinkFromAppUrl',
            input = {'app_url': url}
        )