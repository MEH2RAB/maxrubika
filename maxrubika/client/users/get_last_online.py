from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetLastOnline:
    async def get_last_online(
        self: "maxrubika.Messenger",
        user: str
    ):
        """
        Get the last online status of a user.

        Parameters:
            user (str): The GUID, link, or username of the user.

        Returns:
            Last online status with details.
        """
        from ...data import Data

        user_info = await self.get_user_info(user)

        if isinstance(user_info, dict):
            user_info = Data(user_info)

        online = user_info.find_keys('online_time')

        if not online:
            no_online = {"status": "OK", "online_type": "Unknown"}
            if getattr(self, 'as_dict', False):
                return no_online
            return Data(no_online)

        if isinstance(online, dict):
            online = Data(online)

        online_type = online.find_keys('type')
        result = {"status": "OK", "online_type": online_type}

        if online_type == 'Exact':
            timestamp = online.find_keys('exact_time')
            if timestamp:
                dt = datetime.fromtimestamp(timestamp)
                result["timestamp"] = timestamp
                result["date"] = dt.strftime('%Y-%m-%d')
                result["time"] = dt.strftime('%H:%M:%S')

        elif online_type == 'Approximate':
            period = online.find_keys('approximate_period') or 'Unknown'
            result["period"] = period

        if getattr(self, 'as_dict', False):
            return result

        return Data(result)