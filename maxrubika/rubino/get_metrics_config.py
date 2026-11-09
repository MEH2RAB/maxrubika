from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetMetricsConfig:
    async def get_metrics_config(
        self: "maxrubika.Rubino",
        my_profile: Optional[str] = None
    ):
        """
        Get the metrics/tracking configuration.

        Parameters:
            my_profile (str, optional): The profile to query. Defaults to self.profile_id.

        Returns:
            The response data containing 'enable_tracking' and 'chances' (with 'loading_file_chance' and 'uploading_file_chance').
        """
        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        return await self.request(
            method='getMetricsConfig',
            input={'profile_id': profile_id}
        )