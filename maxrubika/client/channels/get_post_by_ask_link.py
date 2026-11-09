from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetPostByAskLink:
    async def get_post_by_ask_link(
        self: "maxrubika.Messenger",
        url: str
    ):
        """
        Retrieves channel post by ask_join_link (go.rubika.ir link).

        Parameters:
            url (str): The go.rubika.ir link.

        Returns:
            Channel info and message data.
        """
        import base64
        import json
        from ...data import Data
        from ..exceptions import InvalidInput

        if '*' not in url:
            raise InvalidInput("Invalid go.rubika.ir link.")

        encoded = url.split('*')[1]

        if '--join' in encoded:
            encoded = encoded.split('--join')[0]

        encoded = encoded.replace('-', '+').replace('_', '/')
        encoded += '=' * (-len(encoded) % 4)

        try:
            decoded_bytes = base64.b64decode(encoded)
        except Exception:
            raise InvalidInput("Invalid go.rubika.ir link.") from None

        parts = decoded_bytes.split(b'.')
        if len(parts) < 3:
            raise InvalidInput("Invalid link data.")

        payload = parts[1]
        payload = payload.replace(b'-', b'+').replace(b'_', b'/')
        payload += b'=' * (-len(payload) % 4)

        try:
            payload_decoded = base64.b64decode(payload)
            payload_json = json.loads(payload_decoded.decode('utf-8'))
        except Exception:
            raise InvalidInput("Invalid link data.")

        payload_data = Data(payload_json) if not isinstance(payload_json, Data) else payload_json

        open_chat_data = payload_data.find_keys('open_chat_data') or {}

        if isinstance(open_chat_data, dict):
            open_chat_data = Data(open_chat_data)

        message_id = open_chat_data.find_keys('message_id')
        channel_guid = open_chat_data.find_keys('object_guid')

        if not message_id or not channel_guid:
            raise InvalidInput("Invalid link data.")

        channel_info = await self.get_channel_info(channel_guid)

        if isinstance(channel_info, dict):
            channel_info = Data(channel_info)

        channel = channel_info.find_keys('channel') or {}

        if isinstance(channel, dict):
            channel = Data(channel)

        message_result = await self.get_message_info(channel_guid, message_id)

        if isinstance(message_result, dict):
            message_result = Data(message_result)

        share_link = None
        try:
            url_result = await self.get_message_url(channel_guid, message_id)
            if isinstance(url_result, dict):
                url_result = Data(url_result)
            share_link = url_result.find_keys('share_url')
        except Exception:
            pass

        result_dict = {
            "channel_guid": channel.find_keys('channel_guid'),
            "channel_title": channel.find_keys('channel_title'),
            "description": channel.find_keys('description'),
            "username": channel.find_keys('username'),
            "members_count": channel.find_keys('count_members'),
            "message": message_result.find_keys('message'),
        }

        if share_link:
            result_dict["share_link"] = share_link

        result_dict["timestamp"] = message_result.find_keys('timestamp')

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)