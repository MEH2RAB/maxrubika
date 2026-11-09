from typing import Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class SetProfileSetting:
    async def set_profile_setting(
        self: "maxrubika.Rubino",
        story_allow_reply: Optional[str] = None,
        story_save_to_gallery: Optional[bool] = None,
        story_save_to_archive: Optional[bool] = None,
        post_save_to_gallery: Optional[bool] = None,
        allow_tag: Optional[str] = None,
        message_allowed: Optional[str] = None,
        hide_comment_count: Optional[bool] = None,
        hide_like_count: Optional[bool] = None,
        hide_share_count: Optional[bool] = None,
        message_receiver_profile_id: Optional[str] = None,
        show_avatar_full_size: Optional[bool] = None,
        muted_notif: Optional[bool] = None,
        my_profile: Optional[str] = None
    ):
        """
        Update profile settings.

        Parameters:
            story_allow_reply (str, optional): Who can reply to stories.
            story_save_to_gallery (bool, optional): Save stories to gallery.
            story_save_to_archive (bool, optional): Save stories to archive.
            post_save_to_gallery (bool, optional): Save posts to gallery.
            allow_tag (str, optional): Who can tag the profile.
            message_allowed (str, optional): Who can send messages.
            hide_comment_count (bool, optional): Hide comment count.
            hide_like_count (bool, optional): Hide like count.
            hide_share_count (bool, optional): Hide share count.
            message_receiver_profile_id (str, optional): The profile that receives messages.
            show_avatar_full_size (bool, optional): Show the avatar in full size.
            muted_notif (bool, optional): Mute notifications.
            my_profile (str, optional): The profile to update. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        all_settings = {
            'story_allow_reply': story_allow_reply,
            'story_save_to_gallery': story_save_to_gallery,
            'story_save_to_archive': story_save_to_archive,
            'post_save_to_gallery': post_save_to_gallery,
            'allow_tag': allow_tag,
            'message_allowed': message_allowed,
            'hide_comment_count': hide_comment_count,
            'hide_like_count': hide_like_count,
            'hide_share_count': hide_share_count,
            'message_receiver_profile_id': message_receiver_profile_id,
            'show_avatar_full_size': show_avatar_full_size,
            'muted_notif': muted_notif
        }

        settings = {k: v for k, v in all_settings.items() if v is not None}

        if not settings:
            message = "At least one setting must be provided."
            raise InvalidInput(message)

        if 'message_receiver_profile_id' in settings:
            settings['message_receiver_profile_id'] = await self.get_profile_id(settings['message_receiver_profile_id'])

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'settings': settings,
            'updated_parameters': list(settings.keys())
        }

        return await self.request(
            method='setProfileSetting',
            input=input_data
        )