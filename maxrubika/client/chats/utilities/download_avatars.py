import os
import random
from datetime import datetime
from typing import Optional, Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika
    from ....data import Data

class DownloadAvatars:
    async def download_avatars(
        self: "maxrubika.Messenger",
        chat: str,
        save_as: Optional[Union[str, bool]] = None,
        limit: Optional[int] = None
    ) -> Union[List[bytes], "Data", dict]:
        """
        Download all avatars (or a limited number) of a user, group, or channel.

        Parameters:
            chat (str): The GUID, link, or username of the user, group, or channel.
            save_as (str | bool, optional): Directory path to save the files. If True, saves in current directory. If None, returns bytes list.
            limit (int, optional): Maximum number of avatars to download. If None, downloads all.

        Returns:
            List[bytes], Data, or dict: List of binary data, saved file paths, or result.
        """
        from ....data import Data
        from ...exceptions import InvalidInput
        from ...core.configs import PLATFORMS

        if save_as is True:
            save_dir = os.getcwd()
        elif isinstance(save_as, str):
            if not os.path.exists(save_as):
                message = f"Directory does not exist: {save_as}"
                raise InvalidInput(message)
            if not os.path.isdir(save_as):
                message = f"Path is not a directory: {save_as}"
                raise InvalidInput(message)
            save_dir = save_as
        else:
            save_dir = None

        platform = self._original_platform
        platform_config = PLATFORMS.get(platform, {})
        storage_prefix = platform_config.get('storage_prefix', 'messenger')

        chat_guid = await self.get_guid(chat)

        avatars = await self.get_avatars(chat_guid)

        if isinstance(avatars, dict):
            avatars = Data(avatars)

        avatar_list = avatars.find_keys('avatars') or []

        if not avatar_list:
            if save_dir:
                result_dict = {"saved_files": {}, "directory": os.path.abspath(save_dir)}
                if getattr(self, 'as_dict', False):
                    return result_dict
                return Data(result_dict)
            return []

        if limit is not None and limit > 0:
            avatar_list = avatar_list[:limit]

        if not save_dir:
            all_bytes = []
            for avatar_obj in avatar_list:
                avatar = Data(avatar_obj) if isinstance(avatar_obj, dict) else avatar_obj
                main = avatar.find_keys('main')
                if isinstance(main, dict):
                    main = Data(main)
                async with self.connection.session.get(
                    url=f'https://{storage_prefix}{main.find_keys("dc_id")}.iranlms.ir/InternFile.ashx',
                    params={'id': main.find_keys('file_id'), 'ach': main.find_keys('access_hash_rec')}
                ) as response:
                    if response.ok:
                        all_bytes.append(await response.read())
            return all_bytes

        saved_files = {}
        for i, avatar_obj in enumerate(avatar_list):
            avatar = Data(avatar_obj) if isinstance(avatar_obj, dict) else avatar_obj
            main = avatar.find_keys('main')
            if isinstance(main, dict):
                main = Data(main)
            async with self.connection.session.get(
                url=f'https://{storage_prefix}{main.find_keys("dc_id")}.iranlms.ir/InternFile.ashx',
                params={'id': main.find_keys('file_id'), 'ach': main.find_keys('access_hash_rec')}
            ) as response:
                if response.ok:
                    file_data = await response.read()

                    now = datetime.now()
                    date_str = now.strftime("%Y%m%d_%H%M%S")
                    random_str = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                    mime = main.find_keys('mime') or 'jpg'
                    extension = mime.split('/')[-1] if isinstance(mime, str) and '/' in mime else (mime if isinstance(mime, str) else 'jpg')
                    filename = f"{date_str}_{random_str}.{extension}"

                    filepath = os.path.join(save_dir, filename)
                    os.makedirs(save_dir, exist_ok=True)

                    with open(filepath, 'wb') as f:
                        f.write(file_data)

                    saved_files[f"avatar_{i+1}"] = filename

        result_dict = {
            "saved_files": saved_files,
            "total": len(saved_files),
            "directory": os.path.abspath(save_dir)
        }
        if getattr(self, 'as_dict', False):
            return result_dict
        return Data(result_dict)