from typing import Optional, List, Dict, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class LikePost:
    async def like_post(
        self: "maxrubika.Rubino",
        target_profile: Optional[str] = None,
        post: Optional[str] = None,
        post_ids: Optional[List[Dict]] = None,
        my_profile: Optional[str] = None
    ):
        """
        Like one or more posts.

        Parameters:
            target_profile (str, optional): The profile ID or username that owns the post. Use together with 'post'.
            post (str, optional): The post link or post ID. Use together with 'target_profile'.
            post_ids (List[Dict], optional): List of post identifiers for batch like. Each item must contain 'post' (link or ID) and 'target_profile' (profile ID or username). Cannot be used together with 'post' or 'target_profile'.
            my_profile (str, optional): The profile that likes. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        if post_ids is None and post is None:
            message = "Either 'post' + 'target_profile' or 'post_ids' must be provided."
            raise InvalidInput(message)

        if post_ids is not None and (post is not None or target_profile is not None):
            message = "'post_ids' cannot be used together with 'post' or 'target_profile'."
            raise InvalidInput(message)

        if post is not None and target_profile is None:
            message = "'target_profile' is required when 'post' is provided."
            raise InvalidInput(message)

        if target_profile is not None and post is None:
            message = "'post' is required when 'target_profile' is provided."
            raise InvalidInput(message)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        if post_ids is not None:
            normalized_posts = []
            for item in post_ids:
                pid = await self.get_post_id(item.get('post'), my_profile=my_profile)
                tpid = await self.get_profile_id(item.get('target_profile'), my_profile=my_profile)
                normalized_posts.append({
                    'post_id': pid,
                    'post_profile_id': tpid
                })
            post_id_single = None
            target_profile_id_single = None
        else:
            post_id_single = await self.get_post_id(post, my_profile=my_profile)
            target_profile_id_single = await self.get_profile_id(target_profile)
            normalized_posts = None

        if self.api_version == 1:
            if normalized_posts is not None:
                target_ids = normalized_posts
            else:
                target_ids = [{
                    'post_id': post_id_single,
                    'post_profile_id': target_profile_id_single
                }]
            input_data = {
                'profile_id': profile_id,
                'target_post_data_ids': target_ids,
                'action': 'Like'
            }
            method = 'postAction'
        else:
            if normalized_posts is not None:
                message = "Batch like is not supported in API version 0."
                raise InvalidInput(message)
            input_data = {
                'profile_id': profile_id,
                'action_type': 'Like',
                'post_id': post_id_single,
                'post_profile_id': target_profile_id_single
            }
            method = 'likePostAction'

        return await self.request(
            method=method,
            input=input_data
        )