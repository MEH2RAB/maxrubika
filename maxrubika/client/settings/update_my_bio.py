import maxrubika
from ..exceptions import InvalidInput

class UpdateMyBio:
    async def update_my_bio(self: "maxrubika.Client", bio: str):
        """
        Update user's biography.

        Parameters:
            bio (str): The updated biography (max 150 characters).

        Returns:
            The updated user information.

        Raises:
            InvalidInput: If bio exceeds 150 characters.
        """
        if len(bio) > 150:
            raise InvalidInput("'bio' must be 150 characters or less.")

        return await self.request(
            method = 'updateProfile',
            input = {
                'bio': bio,
                'updated_parameters': ['bio']
            }
        )