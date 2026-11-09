import re
import os
import asyncio
import base64
import datetime
import logging
from typing import Optional, Callable, Union, Dict, Any, TYPE_CHECKING

from .file_extensions import FILE_EXTENSIONS

if TYPE_CHECKING:
    import aiohttp
    import maxrubika

logger = logging.getLogger(__name__)

class DownloadFile:
    def _validate_filename(self, name: str) -> Optional[str]:
        if not name or len(name) > 200:
            return None

        invalid_chars = r'[<>:"/\\|?*]'
        if re.search(invalid_chars, name):
            return None
        return name.strip()

    def _validate_path(self, path: str) -> Optional[str]:
        if not path:
            return None

        if not os.path.isabs(path):
            return None

        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
            except Exception:
                return None

        return path

    def _get_file_extension(self, content_type: str) -> str:
        return FILE_EXTENSIONS.get(content_type.lower(), '.bin')

    def _format_size(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    async def _download_with_retry(self, download_url: str) -> bytes:
        import aiohttp
        from .exceptions import Network

        max_retries = getattr(self, 'max_retries', 5)
        last_error = None

        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(download_url) as response:
                        if response.status == 502:
                            logger.warning(
                                f"Bad Gateway (502) - Attempt {attempt + 1}/{max_retries}"
                            )
                            if attempt < max_retries - 1:
                                await asyncio.sleep(2 ** attempt)
                                continue
                            raise Network("Download failed: Server temporarily unavailable.")

                        if response.status != 200:
                            message = f"Download failed: Server error {response.status}"
                            raise Network(message)

                        return await response.read()

            except aiohttp.ClientError as e:
                last_error = e
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Connection issue - Attempt {attempt + 1}/{max_retries}: {e}"
                    )
                    await asyncio.sleep(2 ** attempt)
                    continue
                message = f"Download failed after multiple attempts: {last_error}"
                raise Network(message)

        if last_error:
            raise Exception(f"Download failed: {last_error}")
        return b''

    async def download_file(
        self: "maxrubika.Bot",
        file_id: str,
        name: Optional[str] = None,
        path: Optional[str] = None,
        save_as: bool = False,
        as_base64: bool = False,
        callback: Optional[Callable[[int, int, float], None]] = None
    ) -> Dict[str, Any]:
        """
        Download the file associated with the specified file ID.

        Parameters:
            file_id (str): The identifier of the file to download.
            name (str, optional): Custom filename (without extension).
            path (str, optional): Custom save path (absolute).
            save_as (bool, optional): If True, save to disk. If False, return bytes only. Defaults to False.
            as_base64 (bool, optional): If True, return as base64 encoded string. Only works when save_as=False. Defaults to False.
            callback (callable, optional): Progress callback function(downloaded, total, percent). Defaults to None.

        Returns:
            dict: Contains 'status', and one of 'file_path' (if save_as=True), 'data' (bytes if save_as=False), or 'base64' (if as_base64=True). Also includes 'size'.
        """
        import aiohttp
        from ..data import Data
        from .exceptions import InvalidInput, InvalidAccess

        file_response = await self.get_file(file_id)

        if file_response.get("status") != "OK":
            raise InvalidAccess("Failed to get file info.")

        download_url = file_response["data"]["download_url"]

        async with aiohttp.ClientSession() as session:
            for attempt in range(self.max_retries):
                try:
                    async with session.head(download_url, allow_redirects=True) as head_response:
                        if head_response.status == 502:
                            if attempt < self.max_retries - 1:
                                logger.warning(
                                    f"Getting file info (502) - Attempt {attempt + 1}/{self.max_retries}"
                                )
                                await asyncio.sleep(2 ** attempt)
                                continue
                            content_type = 'application/octet-stream'
                        else:
                            content_type = head_response.headers.get('Content-Type', '')
                        break
                except Exception as e:
                    if attempt < self.max_retries - 1:
                        logger.warning(
                            f"Cannot get file info - Attempt {attempt + 1}/{self.max_retries}: {e}"
                        )
                        await asyncio.sleep(2 ** attempt)
                        continue
                    content_type = 'application/octet-stream'
                    break

            file_ext = self._get_file_extension(content_type)

            if name:
                validated_name = self._validate_filename(name)
                if not validated_name:
                    raise InvalidInput("Invalid filename.")
                filename = validated_name + file_ext
            else:
                date_str = datetime.datetime.now().strftime("%Y%m%d")
                time_str = datetime.datetime.now().strftime("%H%M%S")
                filename = f"{date_str}_{time_str}{file_ext}"

            if save_as:
                if path:
                    validated_path = self._validate_path(path)
                    if not validated_path:
                        raise InvalidInput("Invalid or inaccessible path.")
                    save_path = validated_path
                else:
                    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                    current_path = os.getcwd()
                    save_path = downloads_path if "Microsoft VS Code" in current_path else current_path

                full_path = os.path.join(save_path, filename)
                os.makedirs(save_path, exist_ok=True)

            file_data = await self._download_with_retry(download_url)

            if callback:
                callback(len(file_data), len(file_data), 100.0)

            if save_as:
                with open(full_path, 'wb') as f:
                    f.write(file_data)

                result_dict = {
                    'status': 'OK',
                    'file_path': full_path,
                    'size': self._format_size(len(file_data))
                }
            elif as_base64:
                result_dict = {
                    'status': 'OK',
                    'base64': base64.b64encode(file_data).decode('utf-8'),
                    'size': self._format_size(len(file_data))
                }
            else:
                result_dict = {
                    'status': 'OK',
                    'data': file_data,
                    'size': self._format_size(len(file_data))
                }

            if getattr(self, 'as_dict', False):
                return result_dict
            return Data(result_dict)