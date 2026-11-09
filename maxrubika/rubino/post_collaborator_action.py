from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class PostCollaboratorAction:
    async def post_collaborator_action(
        self: "maxrubika.Rubino",
        target_profile: str,
        post: str,
        action_type: Literal['Accept', 'Deny', 'Remove'],
        my_profile: Optional[str] = None
    ):
        """
        Accept, deny, or remove a collaborator from a post.

        Parameters:
            target_profile (str): The profile ID or username that owns the post.
            post (str): The post link or post ID.
            action_type (Literal['Accept', 'Deny', 'Remove']): The collaboration action. Case-insensitive.
            my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

        Returns:
            The response data.
        """
        from .exceptions import InvalidInput

        action_map = {
            'accept': 'Accept',
            'deny': 'Deny',
            'remove': 'Remove'
        }

        normalized_action = action_map.get(action_type.lower()) if isinstance(action_type, str) else None
        if not normalized_action:
            message = "'action_type' must be 'Accept', 'Deny', or 'Remove'."
            raise InvalidInput(message)

        post_id = await self.get_post_id(post, my_profile=my_profile)
        target_profile_id = await self.get_profile_id(target_profile)

        if my_profile is None:
            profile_id = self.profile_id
        else:
            profile_id = await self.get_profile_id(my_profile)

        input_data = {
            'profile_id': profile_id,
            'post_profile_id': target_profile_id,
            'post_id': post_id,
            'action_type': normalized_action
        }

        return await self.request(
            method='postCollaboratorAction',
            input=input_data
        )