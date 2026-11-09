from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetChannelPostByLink:
    async def get_channel_post_by_link(
        self: "maxrubika.Messenger",
        url: str
    ):
        """
        Retrieves channel post by application URL.

        Parameters:
            url (str): The channel post URL.

        Returns:
            Channel info and message data.
        """
        import re
        from ...data import Data
        from ..exceptions import InvalidInput

        result = await self.request(method='getLinkFromAppUrl', input={'app_url': url})

        if isinstance(result, dict):
            result = Data(result)

        link_data = result.find_keys('link')
        if not link_data:
            raise InvalidInput()

        if isinstance(link_data, dict):
            link_data = Data(link_data)

        open_chat_data = link_data.find_keys('open_chat_data')
        if not open_chat_data:
            raise InvalidInput()

        if isinstance(open_chat_data, dict):
            open_chat_data = Data(open_chat_data)

        message_id = open_chat_data.find_keys('message_id')
        channel_guid = open_chat_data.find_keys('object_guid')

        if not message_id or not channel_guid:
            raise InvalidInput()

        channel_info = await self.get_channel_info(channel_guid)

        if isinstance(channel_info, dict):
            channel_info = Data(channel_info)

        channel = channel_info.find_keys('channel') or {}

        if isinstance(channel, dict):
            channel = Data(channel)

        message_result = await self.get_message_info(channel_guid, message_id)

        if isinstance(message_result, dict):
            message_result = Data(message_result)

        result_dict = {
            "channel_guid": channel.find_keys('channel_guid'),
            "channel_title": channel.find_keys('channel_title'),
            "description": channel.find_keys('description'),
            "username": channel.find_keys('username'),
            "members_count": channel.find_keys('count_members'),
            "message": message_result.find_keys('message'),
            "timestamp": message_result.find_keys('timestamp'),
        }

        if not self._original_platform.startswith('shad'):
            ask_spam_link = await self._get_ask_spam_link(url)
            if ask_spam_link:
                result_dict["ask_spam_link"] = ask_spam_link

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)

    async def _get_ask_spam_link(self, url: str) -> Optional[str]:
        import re

        if self._original_platform.startswith('shad'):
            return None

        if not re.match(r"https://rubika\.ir/\w+/[A-Z]", url):
            return None

        html = await self._fetch_html(url)
        if not html:
            return None

        link_match = re.search(r'var CHANNEL_MESSAGE_LINK="(rubika://[^"]+)"', html)
        if link_match:
            return link_match.group(1).replace("rubika://o.rubika.ir/", "https://go.rubika.ir/")

        link_match = re.search(r'href="(rubika://[^"]+)"', html)
        if link_match:
            return link_match.group(1).replace("rubika://o.rubika.ir/", "https://go.rubika.ir/")

        return None

    async def _fetch_html(self, url: str) -> Optional[str]:
        import aiohttp

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        timeout = aiohttp.ClientTimeout(total=30, connect=10)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, headers=headers, allow_redirects=True) as response:
                    if response.status != 200:
                        return None
                    html = await response.text(encoding='utf-8')
                    if not html or len(html) < 100:
                        return None
                    return html

        except Exception:
            return None