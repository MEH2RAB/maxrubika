from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class CreatePage:
    async def create_page(
        self: "maxrubika.Rubino",
        name: str,
        username: str,
        profile_status: Literal['Public', 'Private'] = 'Public',
        profile_type: Optional[Literal['Business', 'Personal', 'Creator']] = None,
        bio: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        website: Optional[str] = None,
        avatar_file: Optional[str] = None,
        avatar_thumbnail: Optional[str] = None
    ):
        """
        Create a new page (profile).

        Parameters:
            name (str): The display name of the page.
            username (str): The username for the page.
            profile_status (Literal['Public', 'Private']): The page visibility. Case-insensitive. Default is 'Public'.
            profile_type (Literal['Business', 'Personal', 'Creator'], optional): The page type. Case-insensitive.
            bio (str, optional): The page bio.
            email (str, optional): The email contact.
            phone (str, optional): The phone contact.
            website (str, optional): The website contact.
            avatar_file (str, optional): Local path to the avatar main image. If 'avatar_thumbnail' is not provided, the main file is uploaded again as the thumbnail.
            avatar_thumbnail (str, optional): Local path to the avatar thumbnail image.

        Returns:
            The response data.

        Examples:
            # Minimal page
            await client.create_page(
                name="My Page",
                username="mypage"
            )

            # Private business page with bio
            await client.create_page(
                name="My Business",
                username="mybusiness",
                profile_status="Private",
                profile_type="Business",
                bio="We sell stuff"
            )

            # Page with contacts
            await client.create_page(
                name="My Store",
                username="mystore",
                profile_type="Business",
                email="info@example.com",
                phone="+989123456789",
                website="https://example.com"
            )

            # Page with avatar (thumbnail auto-uploaded from main if omitted)
            await client.create_page(
                name="My Page",
                username="mypage",
                avatar_file="avatar.jpg"
            )

            # Page with explicit avatar thumbnail
            await client.create_page(
                name="My Page",
                username="mypage",
                avatar_file="avatar.jpg",
                avatar_thumbnail="avatar_thumb.jpg"
            )
        """
        from ..data import Data

        status_map = {
            'public': 'Public',
            'private': 'Private'
        }
        profile_status = status_map.get(profile_status.lower()) if isinstance(profile_status, str) else None

        type_map = {
            'business': 'Business',
            'personal': 'Personal',
            'creator': 'Creator'
        }
        if profile_type is not None:
            profile_type = type_map.get(profile_type.lower())

        avatar_obj = None
        if avatar_file is not None:
            def _to_file_obj(upload_result):
                if isinstance(upload_result, dict):
                    upload_result = Data(upload_result)
                return {
                    'file_id': upload_result.find_keys('file_id'),
                    'hash_file_receive': upload_result.find_keys('hash_file_receive')
                }

            main_upload = await self.upload_file(avatar_file, 'Picture')
            main_obj = _to_file_obj(main_upload)

            if avatar_thumbnail is not None:
                thumb_upload = await self.upload_file(avatar_thumbnail, 'Picture')
            else:
                thumb_upload = await self.upload_file(avatar_file, 'Picture')

            thumb_obj = _to_file_obj(thumb_upload)

            avatar_obj = {
                'main': main_obj,
                'thumbnail': thumb_obj
            }

        input_data = {
            'username': username,
            'name': name,
            'profile_status': profile_status
        }

        if profile_type is not None:
            input_data['profile_type'] = profile_type

        if bio is not None:
            input_data['bio'] = bio

        if email is not None or phone is not None or website is not None:
            contacts = []
            if email is not None:
                contacts.append({'contact_type': 'Email', 'contact_value': email})
            if phone is not None:
                contacts.append({'contact_type': 'Call', 'contact_value': phone})
            if website is not None:
                contacts.append({'contact_type': 'Website', 'contact_value': website})
            input_data['profile_contacts'] = contacts

        if avatar_obj is not None:
            input_data['avatar_file'] = avatar_obj

        return await self.request(
            method='createProfile',
            input=input_data
        )