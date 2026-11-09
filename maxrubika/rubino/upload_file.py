from typing import Optional, Literal, TYPE_CHECKING
import os

if TYPE_CHECKING:
    import maxrubika

class UploadFile:
    async def upload_file(
        self: "maxrubika.Rubino",
        file: str,
        file_type: Literal["Picture", "Video"] = "Picture",
        mime: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Upload a local file or bytes to Rubino.

        Parameters:
            file (str | bytes): Local path or raw bytes of the file.
            file_type (Literal["Picture", "Video"]): Either 'Picture' or 'Video'.
                Case-insensitive. Defaults to 'Picture'.
            mime (str, optional): MIME type. Defaults based on file_type
                ('jpg' for Picture, 'mp4' for Video).
            my_profile (str, optional): The profile that uploads. Defaults to self.profile_id.

        Returns:
            Data: Upload result containing file_id, hash_file_request, server_url, and hash_file_receive.
        """
        import aiohttp
        import aiofiles
        from ..data import Data

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        if isinstance(file, bytes):
            fallback_name = "maxrubika.jpg" if file_type.lower() in ("picture", "image", "photo") else "maxrubika.mp4"
            total_bytes = len(file)
        else:
            with open(file, "rb") as f:
                f.seek(0, os.SEEK_END)
                total_bytes = f.tell()
            fallback_name = os.path.basename(file)

        if not mime:
            mime = 'jpg' if file_type.lower() in ("picture", "image", "photo") else 'mp4'

        session_info = await self.request_send_file(
            fallback_name, total_bytes, file_type, mime, profile_id
        )

        if isinstance(session_info, dict):
            session_info = Data(session_info)

        upload_url = session_info.find_keys('upload_url') or session_info.find_keys('server_url')
        resource_id = session_info.find_keys('file_id')
        upload_token = session_info.find_keys('hash_file_request')

        block_limit = 131072
        block_count = max(1, (total_bytes + block_limit - 1) // block_limit)
        endpoint_host = upload_url.replace("https://", "").split("/")[0]

        tls = aiohttp.TCPConnector(ssl=False)
        final_packet = None

        async with aiohttp.ClientSession(connector=tls) as http:
            for idx in range(1, block_count + 1):
                offset = block_limit * (idx - 1)

                if isinstance(file, bytes):
                    chunk = file[offset: offset + block_limit]
                else:
                    async with aiofiles.open(file, "rb") as f:
                        await f.seek(offset)
                        chunk = await f.read(block_limit)

                chunk_headers = {
                    "part-number": str(idx),
                    "total-part": str(block_count),
                    "auth": self.auth,
                    "hash-file-request": upload_token,
                    "file-id": str(resource_id),
                    "content-type": "application/octet-stream",
                    "content-length": str(len(chunk)),
                    "Host": endpoint_host,
                    "Connection": "Keep-Alive",
                    "accept-encoding": "gzip",
                    "user-agent": "okhttp/3.12.1"
                }

                while True:
                    try:
                        async with http.post(upload_url, data=chunk, headers=chunk_headers) as resp:
                            if resp.status == 200:
                                final_packet = await resp.json()
                                break
                            else:
                                raise ConnectionError(
                                    f"Upload failed with status {resp.status}"
                                )
                    except aiohttp.ClientConnectionError:
                        raise ConnectionError("Failed to connect to upload server.")

        result_dict = {
            'file_id': resource_id,
            'hash_file_request': upload_token,
            'server_url': upload_url,
            'hash_file_receive': final_packet["data"]["hash_file_receive"]
        }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)