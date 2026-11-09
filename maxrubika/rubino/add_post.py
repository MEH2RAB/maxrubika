from random import randint
from typing import Optional, Literal, TYPE_CHECKING
import os

if TYPE_CHECKING:
    import maxrubika

class AddPost:
    async def add_post(
        self: "maxrubika.Rubino",
        file: str,
        caption: str = '',
        width: int = 1080,
        height: int = 1080,
        thumbnail_file: Optional[str] = None,
        video_duration: Optional[int] = None,
        post_type: Literal['Simple', 'Reels'] = 'Simple',
        my_profile: Optional[str] = None,
        location_id: Optional[str] = None,
        collaborators: Optional[list] = None,
        hide_comment_count: bool = False,
        hide_like_count: bool = False,
        show_only_close_friend: bool = False,
        hide_share_count: bool = False
    ):
        """
        Add a new post to a profile.

        Parameters:
            file (str): Local path to the main picture or video file.
            caption (str, optional): The post caption. Defaults to empty string.
            width (int, optional): The post width in pixels. Default is 1080. For 'Simple' use square or landscape dimensions; for 'Reels' use vertical (e.g. 1080x1920).
            height (int, optional): The post height in pixels. Default is 1080.
            thumbnail_file (str, optional): Local path to a separate thumbnail/cover image. For pictures, defaults to re-uploading the main file. For videos, if not provided, the cover is extracted from the video using MediaThumbnail.
            video_duration (int, optional): Video duration in seconds. Required for videos when MediaThumbnail is not available (optional libraries missing).
            post_type (Literal['Simple', 'Reels']): The post type. Case-insensitive. Default is 'Simple'.
            my_profile (str, optional): The profile that uploads and owns the post. Defaults to self.profile_id.
            location_id (str, optional): The location ID for the post.
            collaborators (list, optional): List of collaborator profile IDs or usernames.
            hide_comment_count (bool, optional): Hide the comment count on the post. Default is False.
            hide_like_count (bool, optional): Hide the like count on the post. Default is False.
            show_only_close_friend (bool, optional): Show the post only to close friends. Default is False.
            hide_share_count (bool, optional): Hide the share count on the post. Default is False.

        Returns:
            The response data.

        Raises:
            InvalidInput: If required optional libraries are missing for video processing without `thumbnail_file`/`video_duration`, or if the file is invalid.

        Examples:
            # Simple square picture post
            await client.add_post(
                file="photo.jpg",
                caption="Hello world!"
            )

            # Reels video post (cover and duration auto-extracted)
            await client.add_post(
                file="reel.mp4",
                caption="A cool reel",
                post_type="Reels",
                width=1080,
                height=1920
            )

            # Reels video with explicit cover and duration in seconds (no optional libraries needed)
            await client.add_post(
                file="reel.mp4",
                caption="Manual cover",
                post_type="Reels",
                width=1080,
                height=1920,
                thumbnail_file="cover.jpg",
                video_duration=15
            )
        """
        from .exceptions import InvalidInput
        from ..data import Data
        from .media import MediaThumbnail

        if not file or not isinstance(file, str):
            raise InvalidInput("'file' must be a non-empty file path.")

        if not os.path.isfile(file):
            raise InvalidInput(f"'file' does not exist: {file}")

        if not isinstance(width, int) or width <= 0:
            raise InvalidInput("'width' must be a positive integer.")

        if not isinstance(height, int) or height <= 0:
            raise InvalidInput("'height' must be a positive integer.")

        type_map = {
            'simple': 'Simple',
            'reels': 'Reels'
        }
        post_type = type_map.get(post_type.lower()) if isinstance(post_type, str) else None

        if not post_type:
            raise InvalidInput("'post_type' must be 'Simple' or 'Reels'.")

        ext = os.path.splitext(file)[1].lower()
        image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        video_exts = {'.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv'}

        if ext in image_exts:
            file_type = 'Picture'
        elif ext in video_exts:
            file_type = 'Video'
        else:
            raise InvalidInput(f"Unsupported file extension: {ext}")

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        def _to_file_obj(upload_result):
            if isinstance(upload_result, dict):
                upload_result = Data(upload_result)
            return {
                'file_id': upload_result.find_keys('file_id'),
                'hash_file_receive': upload_result.find_keys('hash_file_receive')
            }

        def _extract_media_info(video_bytes):
            try:
                info = MediaThumbnail.from_video(video_bytes)
            except Exception as e:
                message = f"Failed to process video with MediaThumbnail: {e}"
                raise InvalidInput(message) from e

            if isinstance(info, str):
                message = "Could not process video: optional libraries (Pillow, OpenCV, MoviePy) are not installed or the video format is unsupported. Please install them or provide 'thumbnail_file' and 'video_duration' explicitly."
                raise InvalidInput(message)

            if info.seconds is None:
                raise InvalidInput("Could not determine video duration. Please provide 'video_duration' explicitly.")

            return info

        main_upload = await self.upload_file(file, file_type, my_profile=my_profile)
        main_obj = _to_file_obj(main_upload)

        if file_type == 'Picture':
            if thumbnail_file is not None:
                if not isinstance(thumbnail_file, str) or not os.path.isfile(thumbnail_file):
                    raise InvalidInput(f"'thumbnail_file' does not exist: {thumbnail_file}")
                thumb_upload = await self.upload_file(thumbnail_file, 'Picture', my_profile=my_profile)
            else:
                thumb_upload = await self.upload_file(file, 'Picture', my_profile=my_profile)

            thumb_obj = _to_file_obj(thumb_upload)

            normalized_file = {
                'file_type': 'Picture',
                'picture_file': {
                    'main': main_obj,
                    'thumbnail': thumb_obj
                }
            }
        else:
            media_info = None

            if thumbnail_file is not None:
                if not isinstance(thumbnail_file, str) or not os.path.isfile(thumbnail_file):
                    raise InvalidInput(f"'thumbnail_file' does not exist: {thumbnail_file}")
                cover_upload = await self.upload_file(thumbnail_file, 'Picture', my_profile=my_profile)
                cover_obj = _to_file_obj(cover_upload)
                thumb_cover_upload = await self.upload_file(thumbnail_file, 'Picture', my_profile=my_profile)
                thumb_cover_obj = _to_file_obj(thumb_cover_upload)
            else:
                with open(file, 'rb') as f:
                    video_bytes = f.read()

                media_info = _extract_media_info(video_bytes)

                cover_upload = await self.upload_file(media_info.image, 'Picture', my_profile=my_profile)
                cover_obj = _to_file_obj(cover_upload)
                thumb_cover_upload = await self.upload_file(media_info.image, 'Picture', my_profile=my_profile)
                thumb_cover_obj = _to_file_obj(thumb_cover_upload)

            if video_duration is None:
                if media_info is None:
                    with open(file, 'rb') as f:
                        video_bytes = f.read()
                    media_info = _extract_media_info(video_bytes)

                video_duration = media_info.seconds // 1000

            normalized_file = {
                'file_type': 'Video',
                'video_file': {
                    'main': main_obj,
                    'cover': cover_obj,
                    'thumbnail_cover': thumb_cover_obj,
                    'duration': video_duration
                }
            }

        input_data = {
            'profile_id': profile_id,
            'file_list': [normalized_file],
            'caption': caption,
            'type': post_type,
            'width': width,
            'height': height,
            'rnd': randint(100000, 999999),
            'post_settings': {
                'hide_comment_count': hide_comment_count,
                'hide_like_count': hide_like_count,
                'show_only_close_friend': show_only_close_friend,
                'hide_share_count': hide_share_count
            }
        }

        if location_id is not None:
            input_data['location_id'] = location_id

        if collaborators is not None:
            normalized_collaborators = []
            for collab in collaborators:
                collab_id = await self.get_profile_id(collab)
                normalized_collaborators.append(collab_id)
            input_data['collaborators'] = normalized_collaborators

        return await self.request(
            method='addPost',
            input=input_data
        )