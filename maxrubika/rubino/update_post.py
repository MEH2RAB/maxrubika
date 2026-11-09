from typing import Optional, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UpdatePost:
    async def update_post(
        self: "maxrubika.Rubino",
        post: str,
        caption: Optional[str] = None,
        location_id: Optional[str] = None,
        update_post_file_list: Optional[List[Dict]] = None,
        hide_comment_count: Optional[bool] = None,
        hide_like_count: Optional[bool] = None,
        show_only_close_friend: Optional[bool] = None,
        hide_share_count: Optional[bool] = None,
        collaborators: Optional[List[str]] = None,
        my_profile: Optional[str] = None
    ):
        """
        Update a post.

        Parameters:
            post (str): The post link or post ID.
            caption (str, optional): The new caption.
            location_id (str, optional): The new location ID.
            update_post_file_list (List[Dict], optional): List of file updates. Each item must contain 'file_index' (int) and may contain 'alt_text', 'tag_list', 'product_list'.
            hide_comment_count (bool, optional): Hide the comment count.
            hide_like_count (bool, optional): Hide the like count.
            show_only_close_friend (bool, optional): Show only to close friends.
            hide_share_count (bool, optional): Hide the share count.
            collaborators (List[str], optional): List of collaborator profile IDs or usernames.
            my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        post_id = await self.get_post_id(post, my_profile=my_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        updated_parameters = []
        input_data = {
            'profile_id': profile_id,
            'post_id': post_id
        }

        if caption is not None:
            input_data['caption'] = caption
            updated_parameters.append('caption')

        if location_id is not None:
            input_data['location_id'] = location_id
            updated_parameters.append('location_id')

        if update_post_file_list is not None:
            input_data['update_post_file_list'] = update_post_file_list
            updated_parameters.append('update_post_file_list')

        if any(v is not None for v in [hide_comment_count, hide_like_count, show_only_close_friend, hide_share_count]):
            input_data['post_settings'] = {
                'hide_comment_count': hide_comment_count if hide_comment_count is not None else False,
                'hide_like_count': hide_like_count if hide_like_count is not None else False,
                'show_only_close_friend': show_only_close_friend if show_only_close_friend is not None else False,
                'hide_share_count': hide_share_count if hide_share_count is not None else False
            }
            updated_parameters.append('post_settings')

        if collaborators is not None:
            normalized_collaborators = []
            for collab in collaborators:
                collab_id = await self.get_profile_id(collab)
                normalized_collaborators.append(collab_id)
            input_data['collaborators'] = normalized_collaborators
            updated_parameters.append('collaborators')

        if not updated_parameters:
            message = "At least one field must be provided to update."
            raise InvalidInput(message)

        input_data['updated_parameters'] = updated_parameters

        return await self.request(
            method='updatePost',
            input=input_data
        )