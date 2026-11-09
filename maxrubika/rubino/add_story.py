from random import randint
from typing import Optional, Literal, TYPE_CHECKING
import os

if TYPE_CHECKING:
    import maxrubika

class AddStory:
    async def add_story(
        self: "maxrubika.Rubino",
        file: str,
        width: int = 1080,
        height: int = 1920,
        thumbnail_file: Optional[str] = None,
        video_duration: Optional[int] = None,
        story_type: Optional[Literal['Picture', 'Video']] = None,
        allow_comment: bool = True,
        show_only_close_friend: bool = False,
        reply_status: Optional[Literal['Following', 'All', 'Nobody']] = None,
        for_close_friend: Optional[list] = None,
        brand_partnership_profile_ids: Optional[list] = None,
        widget_story_list: Optional[list] = None,
        my_profile: Optional[str] = None
    ):
        """
        Add a new story to a profile.

        Parameters:
            file (str): Local path to the main picture or video file.
            width (int, optional): The story width in pixels. Default is 1080.
            height (int, optional): The story height in pixels. Default is 1920.
            thumbnail_file (str, optional): Local path to a separate thumbnail/cover image. For pictures, defaults to re-uploading the main file. For videos, if not provided, the cover is extracted from the video using MediaThumbnail.
            video_duration (int, optional): Video duration in MILLISECONDS. Required for videos when MediaThumbnail is not available.
            story_type (Literal['Picture', 'Video'], optional): The story type. Auto-detected from the file extension if not provided.
            allow_comment (bool, optional): Allow comments on the story. Default is True.
            show_only_close_friend (bool, optional): Show the story only to close friends. Default is False.
            reply_status (Literal['Following', 'All', 'Nobody'], optional): Who can reply to the story. Case-insensitive. Defaults to 'All'.
            for_close_friend (list, optional): List of profile IDs allowed to view the story as close friends.
            brand_partnership_profile_ids (list, optional): List of brand partnership profile IDs.
            widget_story_list (list, optional): List of widget dictionaries (poll, hashtag, mention, emoji_slider, post_to_story, story_link, quiz, count_down, question, story_to_story, add_yours). Each widget must contain 'type' and 'position'.
            my_profile (str, optional): The profile that uploads and owns the story. Defaults to self.profile_id.

        Returns:
            The response data.

        Raises:
            InvalidInput: If required optional libraries are missing for video processing without `thumbnail_file`/`video_duration`, or if the file is invalid.

        Examples:
            # Simple picture story
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest"
            )

            # Video story with explicit cover and duration (milliseconds)
            await client.add_story(
                file="video.mp4",
                thumbnail_file="cover.jpg",
                video_duration=10000,
                my_profile="MAXRubikaTest"
            )

            # Story with custom settings
            await client.add_story(
                file="photo.jpg",
                allow_comment=False,
                show_only_close_friend=True,
                reply_status="Following",
                my_profile="MAXRubikaTest"
            )

            # Story with a Poll widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "Poll",
                    "position": {
                        "point_position": {"x": 0.5, "y": 0.5},
                        "width": 0.6,
                        "height": 0.2,
                        "rotation": 0.0
                    },
                    "poll": {
                        "content": "Which one?",
                        "choices_list": ["Yes", "No"]
                    }
                }]
            )

            # Story with a Hashtag widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "Hashtag",
                    "position": {
                        "point_position": {"x": 0.3, "y": 0.7},
                        "width": 0.4,
                        "height": 0.1,
                        "rotation": 0.0
                    },
                    "hashtag": {"hashtag": "rubika"}
                }]
            )

            # Story with a Mention widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "Mention",
                    "position": {
                        "point_position": {"x": 0.5, "y": 0.6},
                        "width": 0.4,
                        "height": 0.1,
                        "rotation": 0.0
                    },
                    "mention": {"profile_id": "u0abc123def"}
                }]
            )

            # Story with a StoryLink widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "StoryLink",
                    "position": {
                        "point_position": {"x": 0.5, "y": 0.8},
                        "width": 0.6,
                        "height": 0.1,
                        "rotation": 0.0
                    },
                    "story_link": {
                        "link": "https://rubika.ir",
                        "text": "Rubika website"
                    }
                }]
            )

            # Story with a Quiz widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "Quiz",
                    "position": {
                        "point_position": {"x": 0.5, "y": 0.3},
                        "width": 0.7,
                        "height": 0.3,
                        "rotation": 0.0
                    },
                    "quiz": {
                        "content": "Capital of Iran?",
                        "choices_list": ["Tehran", "Isfahan", "Shiraz"],
                        "correct_index": 0
                    }
                }]
            )

            # Story with a CountDown widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "CountDown",
                    "position": {
                        "point_position": {"x": 0.5, "y": 0.5},
                        "width": 0.6,
                        "height": 0.2,
                        "rotation": 0.0
                    },
                    "count_down": {
                        "content": "My birthday!",
                        "timestamp": 1794034607,
                        "is_remind_on": True
                    }
                }]
            )

            # Story with a Question widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "Question",
                    "position": {
                        "point_position": {"x": 0.5, "y": 0.5},
                        "width": 0.6,
                        "height": 0.2,
                        "rotation": 0.0
                    },
                    "question": {"content": "Any questions?"}
                }]
            )

            # Story with an EmojiSlider widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "EmojiSlider",
                    "position": {
                        "point_position": {"x": 0.5, "y": 0.5},
                        "width": 0.6,
                        "height": 0.2,
                        "rotation": 0.0
                    },
                    "emoji_slider": {
                        "content": "How beautiful is this?",
                        "emoji_char": "❤️",
                        "theme": {
                            "background_color": {"red": 255, "green": 255, "blue": 255, "alpha": 255},
                            "text_color": {"red": 0, "green": 0, "blue": 0, "alpha": 255},
                            "seekbar_background_color": {"red": 200, "green": 200, "blue": 200, "alpha": 255},
                            "seekbar_progress_color": {"red": 255, "green": 0, "blue": 0, "alpha": 255},
                            "seekbar_type": "Simple"
                        }
                    }
                }]
            )

            # Story with a PostToStory widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "PostToStory",
                    "position": {
                        "point_position": {"x": 0.5, "y": 0.5},
                        "width": 0.6,
                        "height": 0.6,
                        "rotation": 0.0
                    },
                    "post_to_story": {
                        "post_id": "6aee1d58ca7c95c82981e983",
                        "post_creator_id": "67f65de73b77504d03749be2",
                        "post_profile_id": "67f65de73b77504d03749be2"
                    }
                }]
            )

            # Story with a StoryToStory widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "StoryToStory",
                    "position": {
                        "point_position": {"x": 0.5, "y": 0.5},
                        "width": 0.6,
                        "height": 0.6,
                        "rotation": 0.0
                    },
                    "story_to_story": {
                        "story_id": "6aeecbaff1089881816c7142",
                        "story_creator_id": "6a807217b59333f89d394d36",
                        "story_profile_id": "6a807217b59333f89d394d36"
                    }
                }]
            )

            # Story with an AddYours widget
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[{
                    "type": "AddYours",
                    "position": {
                        "point_position": {"x": 0.5, "y": 0.5},
                        "width": 0.6,
                        "height": 0.3,
                        "rotation": 0.0
                    },
                    "add_yours": {
                        "content": "Send your photo!",
                        "main_story_data": {
                            "story_id": "6aeecbaff1089881816c7142",
                            "story_profile_id": "6a807217b59333f89d394d36"
                        }
                    }
                }]
            )

            # Story with multiple widgets
            await client.add_story(
                file="photo.jpg",
                my_profile="MAXRubikaTest",
                widget_story_list=[
                    {
                        "type": "Poll",
                        "position": {
                            "point_position": {"x": 0.5, "y": 0.3},
                            "width": 0.6,
                            "height": 0.2,
                            "rotation": 0.0
                        },
                        "poll": {
                            "content": "Do you agree?",
                            "choices_list": ["Yes", "No"]
                        }
                    },
                    {
                        "type": "Hashtag",
                        "position": {
                            "point_position": {"x": 0.5, "y": 0.7},
                            "width": 0.4,
                            "height": 0.1,
                            "rotation": 0.0
                        },
                        "hashtag": {"hashtag": "maxrubika"}
                    }
                ]
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

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        ext = os.path.splitext(file)[1].lower()
        image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        video_exts = {'.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv'}

        if ext in image_exts:
            detected_type = 'Picture'
        elif ext in video_exts:
            detected_type = 'Video'
        else:
            raise InvalidInput(f"Unsupported file extension: {ext}")

        if story_type is None:
            story_type = detected_type
        else:
            type_map = {
                'picture': 'Picture',
                'video': 'Video'
            }
            story_type = type_map.get(story_type.lower()) if isinstance(story_type, str) else None
            if not story_type:
                raise InvalidInput("'story_type' must be 'Picture' or 'Video'.")

        reply_status_map = {
            'following': 'Following',
            'all': 'All',
            'nobody': 'Nobody'
        }
        if reply_status is not None:
            reply_status = reply_status_map.get(reply_status.lower()) if isinstance(reply_status, str) else None
            if not reply_status:
                raise InvalidInput("'reply_status' must be 'Following', 'All', or 'Nobody'.")

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

        main_upload = await self.upload_file(file, story_type, my_profile=my_profile)
        main_obj = _to_file_obj(main_upload)

        if story_type == 'Picture':
            if thumbnail_file is not None:
                if not isinstance(thumbnail_file, str) or not os.path.isfile(thumbnail_file):
                    raise InvalidInput(f"'thumbnail_file' does not exist: {thumbnail_file}")
                thumb_upload = await self.upload_file(thumbnail_file, 'Picture', my_profile=my_profile)
            else:
                thumb_upload = await self.upload_file(file, 'Picture', my_profile=my_profile)

            thumb_obj = _to_file_obj(thumb_upload)

            picture_file = {
                'main': main_obj,
                'thumbnail': thumb_obj
            }
            video_file = None
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

                video_duration = media_info.seconds

            picture_file = None
            video_file = {
                'main': main_obj,
                'cover': cover_obj,
                'thumbnail_cover': thumb_cover_obj,
                'duration': video_duration
            }

        story_settings = {
            'allow_comment': allow_comment,
            'show_only_close_friend': show_only_close_friend,
            'reply_status': reply_status if reply_status is not None else 'All'
        }

        input_data = {
            'profile_id': profile_id,
            'story_type': story_type,
            'width': width,
            'height': height,
            'rnd': randint(100000, 999999),
            'story_settings': story_settings
        }

        if picture_file is not None:
            input_data['picture_file'] = picture_file

        if video_file is not None:
            input_data['video_file'] = video_file

        if for_close_friend is not None:
            input_data['for_close_friend'] = for_close_friend

        if brand_partnership_profile_ids is not None:
            input_data['brand_partnership_profile_ids'] = brand_partnership_profile_ids

        if widget_story_list is not None:
            input_data['widget_story_list'] = widget_story_list

        return await self.request(
            method='addStory',
            input=input_data
        )