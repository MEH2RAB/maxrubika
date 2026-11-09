from pathlib import Path
from typing import Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UploadWallpaper:
    async def upload_wallpaper(
        self: "maxrubika.Messenger",
        theme_id: str,
        main_image: Optional[Union[Path, str, bytes]] = None,
        thumbnail_image: Optional[Union[Path, str, bytes]] = None,
        main_file_id: Optional[Union[str, int]] = None,
        main_access_hash_rec: Optional[str] = None,
        thumbnail_file_id: Optional[Union[str, int]] = None,
        thumb_access_hash_rec: Optional[str] = None,
        *args, **kwargs
    ):
        """
        Upload a wallpaper for a theme.

        Parameters:
            theme_id (str): Target theme ID (obtainable via get_themes).
            main_image (Path | str | bytes, optional): The main wallpaper file or bytes.
            thumbnail_image (Path | str | bytes, optional): The thumbnail file or bytes. Reuses main if not provided.
            main_file_id (Union[str, int], optional): Pre-uploaded main wallpaper file ID.
            main_access_hash_rec (str, optional): Pre-uploaded main wallpaper access hash.
            thumbnail_file_id (Union[str, int], optional): Pre-uploaded thumbnail file ID.
            thumb_access_hash_rec (str, optional): Pre-uploaded thumbnail access hash.

        Returns:
            The result of the API call.
        """
        from ...exceptions import InvalidInput

        if not main_file_id or not main_access_hash_rec:
            if main_image is None:
                message = "Either 'main_image' or both 'main_file_id' and 'main_access_hash_rec' must be provided."
                raise InvalidInput(message)

            if isinstance(main_image, (str, Path)):
                kwargs['file_name'] = kwargs.get(
                    'file_name',
                    str(main_image).split('/')[-1]
                )
            else:
                kwargs['file_name'] = kwargs.get('file_name', 'maxrubika.jpg')

            upload = await self.upload_file(main_image, *args, **kwargs)
            main_file_id = upload.file_id
            main_access_hash_rec = upload.access_hash_rec

        if not thumbnail_file_id or not thumb_access_hash_rec:
            if thumbnail_image is not None:
                if isinstance(thumbnail_image, (str, Path)):
                    kwargs['file_name'] = kwargs.get(
                        'file_name',
                        str(thumbnail_image).split('/')[-1]
                    )
                else:
                    kwargs['file_name'] = kwargs.get('file_name', 'maxrubika.jpg')

                upload_thumb = await self.upload_file(thumbnail_image, *args, **kwargs)
                thumbnail_file_id = upload_thumb.file_id
                thumb_access_hash_rec = upload_thumb.access_hash_rec
            else:
                thumbnail_file_id = main_file_id
                thumb_access_hash_rec = main_access_hash_rec

        input_data = {
            'theme_id': theme_id,
            'main_file_id': main_file_id,
            'main_access_hash_rec': main_access_hash_rec,
            'thumbnail_file_id': thumbnail_file_id,
            'thumb_access_hash_rec': thumb_access_hash_rec
        }

        return await self.request(method='addWallpaperSetThemeBackground', input=input_data)