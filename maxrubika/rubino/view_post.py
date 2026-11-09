from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class ViewPost:
    async def view_post(
        self: "maxrubika.Rubino",
        target_profile: str,
        post: str,
        view_duration: int = 5,
        file_list_index: int = 0,
        play_duration: Optional[int] = None,
        track_id: Optional[str] = None,
        my_profile: Optional[str] = None
    ):
        """
        Register a view for a post.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post (str): The post link or post ID.
            view_duration (int, optional): View duration in seconds. Only used in api_version=1. Default is 5.
            file_list_index (int, optional): Index of the file in the post's file list. Only used in api_version=1. Default is 0.
            play_duration (int, optional): Play duration in seconds. Only used in api_version=1.
            track_id (str, optional): Tracking ID for the view. Only used in api_version=1.
            my_profile (str, optional): The profile that views the post. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        post_id = await self.get_post_id(post, my_profile=my_profile)
        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'post_id': post_id,
            'post_profile_id': target_profile_id
        }

        if self.api_version == 1:
            input_data['file_list_index'] = file_list_index
            input_data['view_duration'] = view_duration

            if play_duration is not None:
                input_data['play_duration'] = play_duration

            if track_id is not None:
                input_data['track_id'] = track_id

            method = 'addPostView'
        else:
            method = 'addPostViewCount'

        return await self.request(
            method=method,
            input=input_data
        )