import base64
import json
import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class GetPostByAskLink:
    async def get_post_by_ask_link(
        self: "maxrubika.Client",
        url: str
    ):
        """
        Retrieves channel post by ask_join_link (go.rubika.ir link).

        Parameters:
            url (str): The go.rubika.ir link.

        Returns:
            Channel info and message data.
        """
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
            raise InvalidInput(
                "Invalid go.rubika.ir link."
            ) from None

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

        link_data = payload_json.get('open_chat_data', {})
        message_id = link_data.get('message_id')
        channel_guid = link_data.get('object_guid')

        if not message_id or not channel_guid:
            raise InvalidInput("Invalid link data.")

        channel_info = await self.get_channel_info(channel_guid)
        channel_data = channel_info.to_dict() if hasattr(channel_info, 'to_dict') else channel_info
        channel = channel_data.get('channel', {})

        message_result = await self.get_message_info(channel_guid, message_id)
        message_data = message_result.to_dict() if hasattr(message_result, 'to_dict') else message_result

        share_link = None
        try:
            url_result = await self.get_message_url(channel_guid, message_id)
            url_data = url_result.to_dict() if hasattr(url_result, 'to_dict') else url_result
            share_link = url_data.get('share_url')
        except Exception:
            pass

        result_dict = {
            "channel_guid": channel.get('channel_guid'),
            "channel_title": channel.get('channel_title'),
            "description": channel.get('description'),
            "username": channel.get('username'),
            "members_count": channel.get('count_members'),
            "message": message_data.get('message'),
        }

        if share_link:
            result_dict["share_link"] = share_link

        result_dict["timestamp"] = message_data.get('timestamp')

        return Data(result_dict)