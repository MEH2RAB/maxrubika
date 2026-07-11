import os
import random
from datetime import datetime
from typing import Optional, Union, List
import maxrubika
from ...data import Data
from ..exceptions import InvalidInput

class DownloadProfilePicture:
    async def download_profile_picture(
        self: "maxrubika.Client",
        chat: Optional[str] = None,
        file_id: Optional[str] = None,
        access_hash_rec: Optional[str] = None,
        dc_id: Optional[str] = None,
        save_as: Optional[Union[str, bool]] = None,
        save_all: bool = False,
    ) -> Union[bytes, List[bytes]]:
        """
        Download the profile picture of a user, group, or channel.

        Parameters:
            chat (str, optional): The GUID, link, or username of the user, group, channel, or other chats.
            file_id (str, optional): Direct file_id for download without fetching avatars.
            access_hash_rec (str, optional): Direct access_hash_rec for download without fetching avatars.
            dc_id (str, optional): DC ID required when using file_id and access_hash_rec directly.
            save_as (str or bool, optional): Directory path to save the file(s). If True, saves in current directory. If None, returns bytes only.
            save_all (bool): If True, downloads all avatars instead of just the latest. Returns list of bytes if save_as is None.

        Returns:
            bytes, List[bytes]: Binary data or saved file paths.
        """
        if (file_id and not access_hash_rec) or (access_hash_rec and not file_id):
            message = "Both 'file_id' and 'access_hash_rec' must be provided together."
            raise InvalidInput(message)

        if file_id and access_hash_rec and not dc_id:
            message = "'dc_id' is required when using 'file_id' and 'access_hash_rec' directly."
            raise InvalidInput(message)

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

        if file_id and access_hash_rec and dc_id:
            return await self._download_and_save(
                file_id=file_id,
                access_hash_rec=access_hash_rec,
                dc_id=dc_id,
                save_dir=save_dir,
            )

        if not chat:
            message = "Either 'chat' OR 'file_id' + 'access_hash_rec' + 'dc_id' must be provided."
            raise InvalidInput(message)

        chat_guid = await self.get_guid(chat)

        avatars = await self.get_avatars(chat_guid)

        if not avatars or not avatars.avatars:
            print("No profile picture found.")
            return bytes()

        if save_all:
            avatar_list = avatars.avatars
        else:
            avatar_list = [avatars.avatars[0]]

        if not save_dir:
            if save_all:
                all_bytes = []
                for avatar_obj in avatar_list:
                    avatar = avatar_obj.main
                    async with self.connection.session.get(
                        url=f'https://messenger{avatar.dc_id}.iranlms.ir/InternFile.ashx',
                        params={'id': avatar.file_id, 'ach': avatar.access_hash_rec}
                    ) as response:
                        if response.ok:
                            all_bytes.append(await response.read())
                return all_bytes
            else:
                avatar = avatar_list[0].main
                async with self.connection.session.get(
                    url=f'https://messenger{avatar.dc_id}.iranlms.ir/InternFile.ashx',
                    params={'id': avatar.file_id, 'ach': avatar.access_hash_rec}
                ) as response:
                    if response.ok:
                        return await response.read()
                return bytes()

        saved_files = {}
        for i, avatar_obj in enumerate(avatar_list):
            avatar = avatar_obj.main
            async with self.connection.session.get(
                url=f'https://messenger{avatar.dc_id}.iranlms.ir/InternFile.ashx',
                params={'id': avatar.file_id, 'ach': avatar.access_hash_rec}
            ) as response:
                if response.ok:
                    file_data = await response.read()

                    now = datetime.now()
                    date_str = now.strftime("%Y%m%d_%H%M%S")
                    random_str = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                    mime = getattr(avatar, 'mime', 'jpg')
                    extension = mime.split('/')[-1] if isinstance(mime, str) and '/' in mime else (mime if isinstance(mime, str) else 'jpg')
                    filename = f"{date_str}_{random_str}.{extension}"

                    filepath = os.path.join(save_dir, filename)
                    os.makedirs(save_dir, exist_ok=True)

                    with open(filepath, 'wb') as f:
                        f.write(file_data)

                    saved_files[f"avatar_{i+1}"] = filename

        result_dict = {
            "saved_files": saved_files,
            "directory": os.path.abspath(save_dir)
        }

        return Data(result_dict)

    async def _download_and_save(
            self,
            file_id: str,
            access_hash_rec: str,
            dc_id: str,
            save_dir: Optional[str] = None,
    ) -> Union[bytes, Data]:

        async with self.connection.session.get(
            url=f'https://messenger{dc_id}.iranlms.ir/InternFile.ashx',
            params={'id': file_id, 'ach': access_hash_rec}
        ) as response:
            if response.ok:
                file_data = await response.read()

                if not save_dir:
                    return file_data

                now = datetime.now()
                date_str = now.strftime("%Y%m%d_%H%M%S")
                random_str = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                filename = f"{date_str}_{random_str}.jpg"

                filepath = os.path.join(save_dir, filename)
                os.makedirs(save_dir, exist_ok=True)

                with open(filepath, 'wb') as f:
                    f.write(file_data)

                result_dict = {
                    "saved_files": {"avatar_1": filename},
                    "directory": os.path.abspath(save_dir)
                }

                return Data(result_dict)

            return bytes() if not save_dir else Data({"saved_files": {}, "directory": os.path.abspath(save_dir)})