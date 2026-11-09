from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UpdatePage:
    async def update_page(
        self: "maxrubika.Rubino",
        name: Optional[str] = None,
        username: Optional[str] = None,
        profile_status: Optional[Literal['Public', 'Private']] = None,
        profile_type: Optional[Literal['Business', 'Personal', 'Creator']] = None,
        bio: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        website: Optional[str] = None,
        avatar_file: Optional[str] = None,
        avatar_thumbnail: Optional[str] = None,
        delete_avatar: bool = False,
        my_profile: Optional[str] = None
    ):
        """
        Update a page (profile).

        Only the fields that are provided (not None) will be updated. Contact fields are merged: providing an empty string removes that contact type, while other existing contacts are preserved.

        Parameters:
            name (str, optional): The new display name.
            username (str, optional): The new username.
            profile_status (Literal['Public', 'Private'], optional): The new visibility. Case-insensitive.
            profile_type (Literal['Business', 'Personal', 'Creator'], optional): The new page type. Case-insensitive.
            bio (str, optional): The new bio.
            email (str, optional): The new email contact. If empty string, removes the email contact.
            phone (str, optional): The new phone contact. If empty string, removes the phone contact.
            website (str, optional): The new website contact. If empty string, removes the website contact.
            avatar_file (str, optional): Local path to the new avatar main image. If 'avatar_thumbnail' is not provided, the main file is uploaded again as the thumbnail. Cannot be used together with 'delete_avatar'.
            avatar_thumbnail (str, optional): Local path to the new avatar thumbnail image.
            delete_avatar (bool, optional): If True, removes the current avatar. Cannot be used together with 'avatar_file'. Default is False.
            my_profile (str, optional): The profile to update. Defaults to self.profile_id.

        Returns:
            The response data.

        Examples:
            # Update name only
            await client.update_page(name="New Name")

            # Update bio and status
            await client.update_page(
                bio="New bio",
                profile_status="Private"
            )

            # Update contacts individually
            await client.update_page(
                email="info@example.com",
                phone="9986",
                website="https://example.com"
            )

            # Remove a single contact
            await client.update_page(email="")

            # Update avatar (thumbnail auto-uploaded from main if omitted)
            await client.update_page(
                avatar_file="new_avatar.jpg"
            )

            # Update avatar with explicit thumbnail
            await client.update_page(
                avatar_file="new_avatar.jpg",
                avatar_thumbnail="new_avatar_thumb.jpg"
            )

            # Delete the current avatar
            await client.update_page(delete_avatar=True)
        """
        from .exceptions import InvalidInput
        from ..data import Data

        if delete_avatar and avatar_file is not None:
            raise InvalidInput("'delete_avatar' cannot be used together with 'avatar_file'.")

        updated_parameters = []
        input_data = {}

        if name is not None:
            input_data['name'] = name
            updated_parameters.append('name')

        if username is not None:
            input_data['username'] = username
            updated_parameters.append('username')

        if profile_status is not None:
            status_map = {
                'public': 'Public',
                'private': 'Private'
            }
            normalized_status = status_map.get(profile_status.lower()) if isinstance(profile_status, str) else None
            input_data['profile_status'] = normalized_status or profile_status
            updated_parameters.append('profile_status')

        if profile_type is not None:
            type_map = {
                'business': 'Business',
                'personal': 'Personal',
                'creator': 'Creator'
            }
            normalized_type = type_map.get(profile_type.lower()) if isinstance(profile_type, str) else None
            input_data['profile_type'] = normalized_type or profile_type
            updated_parameters.append('profile_type')

        if bio is not None:
            input_data['bio'] = bio
            updated_parameters.append('bio')

        if email is not None or phone is not None or website is not None:
            contacts = []
            if email is not None:
                contacts.append({'contact_type': 'Email', 'contact_value': email})
            if phone is not None:
                contacts.append({'contact_type': 'Call', 'contact_value': phone})
            if website is not None:
                contacts.append({'contact_type': 'Website', 'contact_value': website})
            input_data['profile_contacts'] = contacts
            updated_parameters.append('profile_contacts')

        if avatar_file is not None:
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

            input_data['avatar_file'] = {
                'main': main_obj,
                'thumbnail': thumb_obj
            }
            updated_parameters.append('avatar_file')
        elif delete_avatar:
            input_data['avatar_file'] = None
            updated_parameters.append('avatar_file')

        if not updated_parameters:
            raise InvalidInput("At least one field must be provided to update.")

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data['profile_id'] = profile_id
        input_data['updated_parameters'] = updated_parameters

        return await self.request(
            method='updateProfile',
            input=input_data
        )