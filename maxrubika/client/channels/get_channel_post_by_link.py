from typing import Optional
import aiohttp
import re
import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class GetChannelPostByLink:
    async def get_channel_post_by_link(
        self: "maxrubika.Client",
        url: str
    ):
        """
        Retrieves channel post by application URL.

        Parameters:
            url (str): The channel post URL.

        Returns:
            Channel info and message data.
        """
        result = await self.request(method='getLinkFromAppUrl', input={'app_url': url})
        info = result.to_dict() if hasattr(result, 'to_dict') else result

        if 'link' not in info:
            raise InvalidInput()

        link_data = info['link']

        if 'open_chat_data' not in link_data:
            raise InvalidInput()

        open_chat_data = link_data['open_chat_data']

        if 'message_id' not in open_chat_data or 'object_guid' not in open_chat_data:
            raise InvalidInput()

        message_id = open_chat_data['message_id']
        channel_guid = open_chat_data['object_guid']

        channel_info = await self.get_channel_info(channel_guid)
        channel_data = channel_info.to_dict() if hasattr(channel_info, 'to_dict') else channel_info
        channel = channel_data.get('channel', {})

        message_result = await self.get_message_info(channel_guid, message_id)
        message_data = message_result.to_dict() if hasattr(message_result, 'to_dict') else message_result

        ask_spam_link = await self._get_ask_spam_link(url)

        result_dict = {
            "channel_guid": channel.get('channel_guid'),
            "channel_title": channel.get('channel_title'),
            "description": channel.get('description'),
            "username": channel.get('username'),
            "members_count": channel.get('count_members'),
            "message": message_data.get('message'),
            "ask_spam_link": ask_spam_link,
            "timestamp": message_data.get('timestamp'),
        }
        return Data(result_dict)

    async def _get_ask_spam_link(self, url: str) -> Optional[str]:
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