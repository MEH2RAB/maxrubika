from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ProfileCreatedAt:
    async def profile_created_at(
        self: "maxrubika.Rubino",
        target_profile: str
    ):
        """
        Get the creation date of a profile.

        Parameters:
            target_profile (str): The profile ID or username.

        Returns:
            Creation date with details.
        """
        from datetime import datetime
        from ..data import Data

        profile_id = await self.get_profile_id(target_profile)

        timestamp = int(profile_id[:8], 16)
        dt = datetime.fromtimestamp(timestamp)

        result_dict = {
            "status": "OK",
            "timestamp": timestamp,
            "date": dt.strftime('%Y-%m-%d'),
            "time": dt.strftime('%H:%M:%S')
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)