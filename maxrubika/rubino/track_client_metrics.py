from typing import Optional, Literal, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class TrackClientMetrics:
    async def track_client_metrics(
        self: "maxrubika.Rubino",
        network: Literal['WiFi', '2G', '3G', '4G', '5G', 'Offline'],
        metrics: List[Dict],
        my_profile: Optional[str] = None
    ):
        """
        Track client metrics for analytics.

        Parameters:
            network (Literal['WiFi', '2G', '3G', '4G', '5G', 'Offline']): The current network type. Case-insensitive.
            metrics (List[Dict]): List of metric entries. Each entry must contain 'type' ('LoadingFile' or 'UploadingFile') and the corresponding data ('loading_file_data' for LoadingFile, 'uploading_file_data' for UploadingFile).
            my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

        Returns:
            The response data.

        Examples:
            # Upload metrics for a successful image upload
            await client.track_client_metrics(
                network="WiFi",
                metrics=[
                    {
                        "type": "UploadingFile",
                        "uploading_file_data": {
                            "status": "Success",
                            "media_type": "Image",
                            "file_size_bytes": 123456,
                            "upload_ms": 1500,
                            "convert_ms": 200,
                            "publish_ms": 300,
                            "total_ms": 2000,
                            "attempts_count": 1,
                            "media_count": 1,
                            "video_count": 0,
                            "is_foreground": True,
                            "is_streaming_upload": False,
                            "stalled": False
                        }
                    }
                ],
                my_profile="MAXRubikaTest"
            )

            # Upload metrics for a failed video upload
            await client.track_client_metrics(
                network="4G",
                metrics=[
                    {
                        "type": "UploadingFile",
                        "uploading_file_data": {
                            "status": "Failed",
                            "media_type": "Video",
                            "file_size_bytes": 5242880,
                            "upload_ms": 12000,
                            "total_ms": 15000,
                            "attempts_count": 3,
                            "media_count": 1,
                            "video_count": 1,
                            "video_duration_ms": 30000,
                            "is_foreground": True,
                            "stalled": True,
                            "stalled_stage": "UploadingFile",
                            "failed_stage": "UploadingFile",
                            "error_type": "NetworkError",
                            "error_detail": "Connection timed out"
                        }
                    }
                ],
                my_profile="MAXRubikaTest"
            )

            # Loading metrics for a video viewed in feed
            await client.track_client_metrics(
                network="WiFi",
                metrics=[
                    {
                        "type": "LoadingFile",
                        "loading_file_data": {
                            "view_type": "Reels",
                            "downloaded_bytes": 1048576,
                            "loading_count": 1,
                            "reached_first_frame": True,
                            "startup_ms": 500,
                            "startup_buffering_ms": 200,
                            "rebuffer_ms": 100,
                            "watch_ms": 8000
                        }
                    }
                ],
                my_profile="MAXRubikaTest"
            )

            # Multiple metrics in one request
            await client.track_client_metrics(
                network="WiFi",
                metrics=[
                    {
                        "type": "UploadingFile",
                        "uploading_file_data": {
                            "status": "Success",
                            "media_type": "Image",
                            "file_size_bytes": 200000,
                            "upload_ms": 1000,
                            "total_ms": 1500,
                            "attempts_count": 1
                        }
                    },
                    {
                        "type": "LoadingFile",
                        "loading_file_data": {
                            "view_type": "Simple",
                            "downloaded_bytes": 500000,
                            "reached_first_frame": True,
                            "startup_ms": 300,
                            "watch_ms": 4000
                        }
                    }
                ],
                my_profile="MAXRubikaTest"
            )
        """
        from .exceptions import InvalidInput

        network_map = {
            'wifi': 'WiFi',
            '2g': '2G',
            '3g': '3G',
            '4g': '4G',
            '5g': '5G',
            'offline': 'Offline'
        }

        normalized_network = network_map.get(network.lower()) if isinstance(network, str) else None
        if not normalized_network:
            message = "'network' must be 'WiFi', '2G', '3G', '4G', '5G', or 'Offline'."
            raise InvalidInput(message)

        if not isinstance(metrics, list):
            message = "'metrics' must be a list."
            raise InvalidInput(message)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'network': normalized_network,
            'metrics': metrics
        }

        return await self.request(
            method='trackClientMetrics',
            input=input_data
        )