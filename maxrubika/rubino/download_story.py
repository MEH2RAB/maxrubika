from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class DownloadStory:
    async def download_story(
        self: "maxrubika.Rubino",
        target_profile: str,
        save_as: bool = True,
        file_name: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Download all stories of a profile.

        Parameters:
            target_profile (str): The profile ID or username that owns the stories.
            save_as (bool, optional): If True, save files to disk; if False, return raw bytes. Default is True.
            file_name (str, optional): Base name for saved files (without extension). If not provided, the current date and time are used.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            Data: Contains 'files' (list of saved paths if save_as=True, otherwise list of dicts with 'file_name' and 'content').
        """
        import aiohttp
        from ..data import Data
        from .exceptions import StoryNotFound

        stories_data = await self.get_profile_stories(
            target_profile=target_profile,
            my_profile=my_profile
        )

        if isinstance(stories_data, dict):
            stories_data = Data(stories_data)

        stories = stories_data.find_keys('stories') or []

        if not stories:
            raise StoryNotFound()

        if file_name is None:
            file_name = datetime.now().strftime('%Y%m%d_%H%M%S')

        files = []

        for story in stories:
            story = Data(story) if isinstance(story, dict) else story

            story_type = story.find_keys('story_type')

            if story_type == 'Picture':
                picture_file = story.find_keys('picture_file')
                if isinstance(picture_file, dict):
                    picture_file = Data(picture_file)
                url = picture_file.find_keys('picture_url')
                ext = '.jpg'
            elif story_type == 'Video':
                video_file = story.find_keys('video_file')
                if isinstance(video_file, dict):
                    video_file = Data(video_file)
                url = video_file.find_keys('video_url')
                ext = '.mp4'
            else:
                continue

            if url:
                files.append({'url': url, 'ext': ext})

        if not files:
            raise StoryNotFound()

        results = []

        async with aiohttp.ClientSession() as session:
            for index, entry in enumerate(files):
                async with session.get(entry['url']) as resp:
                    if resp.status != 200:
                        continue
                    content = await resp.read()

                suffix = f"_{index}" if len(files) > 1 else ""
                current_name = f"{file_name}{suffix}{entry['ext']}"

                if save_as:
                    with open(current_name, 'wb') as f:
                        f.write(content)
                    results.append(current_name)
                else:
                    results.append({
                        'file_name': current_name,
                        'content': content
                    })

        if not results:
            raise StoryNotFound()

        result_dict = {
            'status': 'OK',
            'files': results
        }

        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)