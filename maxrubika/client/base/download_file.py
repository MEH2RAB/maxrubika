import os
import asyncio
import inspect
import aiohttp
import aiofiles
from typing import Callable, Optional, Union
import maxrubika
from .. import exceptions

class DownloadFile:
    async def download_file(
        self: "maxrubika.Client",
        dc_id: int,
        file_id: int,
        access_hash: str,
        size: int,
        chunk: int = 131072,
        callback: Optional[Callable[[int, int], Union[None, asyncio.Future]]] = None,
        gather: bool = False,
        save_as: Optional[Union[str, bool]] = None,
        file_name: Optional[str] = None,
        *args,
        **kwargs,
    ) -> Union[bytes, str]:
        """
        Download a file from Rubika using its file ID and access hash.

        Parameters:
            dc_id (int): Data center ID.
            file_id (int): Unique identifier of the file.
            access_hash (str): Access hash associated with the file.
            size (int): Total size of the file in bytes.
            chunk (int, optional): Size of each download chunk (default: 131072).
            callback (callable, optional): Progress callback(total_size, downloaded_size).
            gather (bool, optional): Download chunks in parallel (default: False).
            save_as (str or bool, optional): Directory path or True for current dir. If None, returns bytes.
            file_name (str, optional): Custom file name.

        Returns:
            bytes or str: File content (bytes) or saved path (str).
        """
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
        base_url = f"https://messenger{dc_id}.iranlms.ir"

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
                
                if os.path.exists(filepath):
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(os.path.join(save_dir, f"{base}_{counter}{ext}")):
                        counter += 1
                    filename = f"{base}_{counter}{ext}"
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
                return filepath

            elif gather:
                tasks = [
                    fetch_chunk(session, start, min(start + chunk, size) - 1)
                    for start in range(0, size, chunk)
                ]
                chunks = await asyncio.gather(*tasks)
                result = b"".join(filter(None, chunks))
                await handle_callback(size, len(result))
                return result

            else:
                result = bytearray()
                for start in range(0, size, chunk):
                    end = min(start + chunk, size) - 1
                    data = await fetch_chunk(session, start, end)
                    if not data:
                        break
                    result.extend(data)
                    await handle_callback(size, len(result))
                return bytes(result)