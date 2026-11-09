from datetime import datetime
from typing import Optional, TYPE_CHECKING
import re

if TYPE_CHECKING:
    import maxrubika

class DownloadPost:
    async def download_post(
        self: "maxrubika.Rubino",
        post: str,
        target_profile: Optional[str] = None,
        save_as: bool = True,
        file_name: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Download all media files of a post.

        Parameters:
            post (str): The post link or post ID.
            target_profile (str, optional): The profile ID or username that owns the post. Required when 'post' is a post ID.
            save_as (bool, optional): If True, save files to disk; if False, return raw bytes. Default is True.
            file_name (str, optional): Base name for saved files (without extension). If not provided, the current date and time are used.
            my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

        Returns:
            Contains 'files' (list of saved paths if save_as=True, otherwise list of dicts with 'file_name' and 'content').
        """
        import aiohttp
        from ..data import Data
        from .exceptions import InvalidInput, PostNotAccessible

        if re.match(r'^[0-9a-f]{24}$', post):
            if target_profile is None:
                message = "'target_profile' is required when 'post' is a post ID."
                raise InvalidInput(message)

            link_result = await self.get_post_link(
                target_profile=target_profile,
                post_id=post,
                my_profile=my_profile
            )

            if isinstance(link_result, dict):
                link_result = Data(link_result)

            share_url = link_result.find_keys('share_url')

            if not share_url:
                message = "Could not retrieve the share link for the given post ID."
                raise InvalidInput(message)

            post = share_url

        post_data = await self.get_post_by_link(post, my_profile=my_profile)

        if isinstance(post_data, dict):
            post_data = Data(post_data)

        if post_data.find_keys('has_access') is False:
            raise PostNotAccessible()

        post_obj = post_data.find_keys('post')

        if not post_obj:
            message = "Post not found or invalid link."
            raise InvalidInput(message)

        if isinstance(post_obj, dict):
            post_obj = Data(post_obj)

        files = []

        main_url = post_obj.find_keys('full_file_url')
        main_type = post_obj.find_keys('file_type')
        if main_url:
            files.append({
                'url': main_url,
                'ext': '.jpg' if main_type == 'Picture' else '.mp4'
            })

        file_list = post_obj.find_keys('file_list') or []
        for item in file_list:
            item = Data(item) if isinstance(item, dict) else item
            item_url = item.find_keys('full_file_url')
            item_type = item.find_keys('file_type')
            if item_url:
                files.append({
                    'url': item_url,
                    'ext': '.jpg' if item_type == 'Picture' else '.mp4'
                })

        if file_name is None:
            file_name = datetime.now().strftime('%Y%m%d_%H%M%S')

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
            raise PostNotAccessible()

        result_dict = {
            'status': 'OK',
            'files': results
        }

        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)