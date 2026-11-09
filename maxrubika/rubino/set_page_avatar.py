from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetPageAvatar:
    async def set_page_avatar(
        self: "maxrubika.Rubino",
        avatar_file: str,
        avatar_thumbnail: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Set or update the avatar of a page (profile).

        Parameters:
            avatar_file (str): Local path to the new avatar main image.
            avatar_thumbnail (str, optional): Local path to the new avatar thumbnail image. If not provided, the main file is uploaded again as the thumbnail.
            my_profile (str, optional): The profile to update. Defaults to self.profile_id.

        Returns:
            The response data.

        Examples:
            # Set avatar (thumbnail auto-uploaded from main)
            await client.set_page_avatar(
                avatar_file="avatar.jpg",
                my_profile="MAXRubikaTest"
            )

            # Set avatar with explicit thumbnail
            await client.set_page_avatar(
                avatar_file="avatar.jpg",
                avatar_thumbnail="avatar_thumb.jpg",
                my_profile="MAXRubikaTest"
            )
        """
        from ..data import Data

        main_upload = await self.upload_file(avatar_file, 'Picture', my_profile=my_profile)
        if isinstance(main_upload, dict):
            main_upload = Data(main_upload)
        main_obj = {
            'file_id': main_upload.find_keys('file_id'),
            'hash_file_receive': main_upload.find_keys('hash_file_receive')
        }

        if avatar_thumbnail is not None:
            thumb_upload = await self.upload_file(avatar_thumbnail, 'Picture', my_profile=my_profile)
        else:
            thumb_upload = await self.upload_file(avatar_file, 'Picture', my_profile=my_profile)

        if isinstance(thumb_upload, dict):
            thumb_upload = Data(thumb_upload)
        thumb_obj = {
            'file_id': thumb_upload.find_keys('file_id'),
            'hash_file_receive': thumb_upload.find_keys('hash_file_receive')
        }

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'avatar_file': {
                'main': main_obj,
                'thumbnail': thumb_obj
            },
            'updated_parameters': ['avatar_file']
        }

        return await self.request(
            method='updateProfile',
            input=input_data
        )