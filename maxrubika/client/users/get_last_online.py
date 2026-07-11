import maxrubika
from datetime import datetime
from ...data import Data
from ..exceptions import InvalidInput

class GetLastOnline:
    async def get_last_online(
        self: "maxrubika.Client",
        user: str
    ):
        """
        Get the last online status of a user.

        Parameters:
            user (str): The GUID, link, or username of the user.

        Returns:
            Last online status with details.
        """
        user_info = await self.get_user_info(user)
        user_data = user_info.to_dict() if hasattr(user_info, 'to_dict') else user_info

        user_obj = user_data.get('user', {})
        online = user_obj.get('online_time', {})

        if not online:
            return Data({"status": "OK", "online_type": "Unknown"})

        online_type = online.get('type', '')
        result = {"status": "OK", "online_type": online_type}

        if online_type == 'Exact':
            timestamp = online.get('exact_time')
            if timestamp:
                dt = datetime.fromtimestamp(timestamp)
                result["timestamp"] = timestamp
                result["date"] = dt.strftime('%Y-%m-%d')
                result["time"] = dt.strftime('%H:%M:%S')

        elif online_type == 'Approximate':
            period = online.get('approximate_period', 'Unknown')
            result["period"] = period

        return Data(result)