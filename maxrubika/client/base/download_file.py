import os
import asyncio
import inspect
import aiohttp
import aiofiles
import base64
from typing import Callable, Optional, Union
import maxrubika
from ...data import Data
from .. import exceptions
from ..core.configs import PLATFORMS

class DownloadFile:
    async def download_file(
        self: "maxrubika.Client",
        file_inline: Optional[Union[dict, Data]] = None,
        dc_id: Optional[int] = None,
        file_id: Optional[int] = None,
        access_hash: Optional[str] = None,
        size: Optional[int] = None,
        chunk: int = 131072,
        callback: Optional[Callable[[int, int], Union[None, asyncio.Future]]] = None,
        gather: bool = False,
        save_as: Optional[Union[str, bool]] = None,
        file_name: Optional[str] = None,
        as_base64: bool = False,
        *args,
        **kwargs,
    ) -> Union[bytes, str, Data]:
        """
        Download a file from Rubika/Shad.

        Parameters:
            file_inline (dict or Data, optional): File inline object from messages.
                If provided, dc_id, file_id, access_hash, size will be extracted.
            dc_id (int, optional): Data center ID (if file_inline not provided).
            file_id (int, optional): Unique identifier of the file.
            access_hash (str, optional): Access hash associated with the file.
            size (int, optional): Total size of the file in bytes.
            chunk (int, optional): Size of each download chunk (default: 131072).
            callback (callable, optional): Progress callback(total_size, downloaded_size).
            gather (bool, optional): Download chunks in parallel (default: False).
            save_as (str or bool, optional): Directory path or True for current dir. If None, returns bytes.
            file_name (str, optional): Custom file name.
            as_base64 (bool, optional): Return as base64 encoded string (default: False).

        Returns:
            bytes, str, or Data: File content (bytes), base64 string, or Data object (when save_as used).
        """
        if file_inline:
            if isinstance(file_inline, Data):
                fi = file_inline
            elif isinstance(file_inline, dict):
                fi = Data(file_inline)
            else:
                raise exceptions.InvalidInput("'file_inline' must be a dict or Data object.")
            dc_id = fi.dc_id
            file_id = fi.file_id
            access_hash = fi.access_hash_rec
            size = fi.size
            if not file_name:
                file_name = fi.get('file_name')
        
        if not all([dc_id, file_id, access_hash, size]):
            raise exceptions.InvalidInput(
                "Either 'file_inline' or all of 'dc_id', 'file_id', 'access_hash', 'size' must be provided."
            )

        if save_as is True:
            save_dir = os.getcwd()
        elif isinstance(save_as, str):
            save_dir = save_as
        else:
            save_dir = None

        max_retries = self.max_retries
        headers = {
            "auth": self.auth,
            "access-hash-rec": access_hash,
            "file-id": str(file_id),
            "user-agent": self.user_agent,
        }

        platform = self._original_platform
        platform_config = PLATFORMS.get(platform, {})
        storage_prefix = platform_config.get('storage_prefix', 'messenger')
        base_url = f"https://{storage_prefix}{dc_id}.iranlms.ir"

        async def fetch_chunk(session, start: int, end: int) -> bytes:
            chunk_headers = {
                **headers,
                "start-index": str(start),
                "last-index": str(end),
            }
            for attempt in range(max_retries):
                try:
                    async with session.post(
                        "/GetFile.ashx", headers=chunk_headers, proxy=self.proxy
                    ) as resp:
                        if resp.status == 200:
                            return await resp.read()
                        self.logger.warning(
                            f"Download failed with status {resp.status}"
                        )
                except Exception as e:
                    self.logger.warning(
                        f"Error downloading chunk {start}-{end} (Attempt {attempt+1}): {e}"
                    )
                await asyncio.sleep(2 ** attempt)
            return b""

        async def handle_callback(total: int, current: int):
            if not callable(callback):
                return
            try:
                if inspect.iscoroutinefunction(callback):
                    await callback(total, current)
                else:
                    callback(total, current)
            except Exception as e:
                self.logger.error(f"Callback error: {e}")

        async with aiohttp.ClientSession(
            base_url=base_url, connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            if save_dir:
                filename = file_name or "download.bin"
                filepath = os.path.join(save_dir, filename)
                os.makedirs(save_dir, exist_ok=True)

                async with aiofiles.open(filepath, "wb") as f:
                    for start in range(0, size, chunk):
                        end = min(start + chunk, size) - 1
                        data = await fetch_chunk(session, start, end)
                        if not data:
                            break
                        await f.write(data)
                        await handle_callback(size, end + 1)
                
                return Data({
                    "status": "OK",
                    "message": f"File saved to {filepath}",
                })

            elif gather:
                tasks = [
                    fetch_chunk(session, start, min(start + chunk, size) - 1)
                    for start in range(0, size, chunk)
                ]
                chunks = await asyncio.gather(*tasks)
                result = b"".join(filter(None, chunks))
                await handle_callback(size, len(result))
                return base64.b64encode(result).decode() if as_base64 else result

            else:
                result = bytearray()
                for start in range(0, size, chunk):
                    end = min(start + chunk, size) - 1
                    data = await fetch_chunk(session, start, end)
                    if not data:
                        break
                    result.extend(data)
                    await handle_callback(size, len(result))
                result = bytes(result)
                return base64.b64encode(result).decode() if as_base64 else result