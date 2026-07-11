from typing import List, Optional
import maxrubika
from ..exceptions import InvalidInput

class RequestVoiceCall:
    async def request_voice_call(
        self: "maxrubika.Client",
        user: str,
        library_versions: Optional[List[str]] = None,
        max_layer: int = 92,
        min_layer: int = 65,
        sip_version: int = 1,
        support_call_out: bool = True
    ):
        """
        Request a voice call with a user.

        Parameters:
            user (str): The GUID or username of the user to call.
            library_versions (List[str], optional): List of supported library versions. Default: ['2.7.7', '2.4.4']
            max_layer (int): Maximum protocol layer. Default: 92
            min_layer (int): Minimum protocol layer. Default: 65
            sip_version (int): SIP version. Default: 1
            support_call_out (bool): Support outgoing calls. Default: True

        Returns:
            Call request result containing session info.
        """
        user_guid = await self.get_guid(user)

        if not user_guid.startswith("u0"):
            message = f"'{user}' does not point to a valid user. Expected a user GUID or username."
            raise InvalidInput(message)

        if library_versions is None:
            library_versions = ['2.7.7', '2.4.4']

        return await self.request(
            method = 'requestCall',
            input = {
                'call_type': 'Voice',
                'library_versions': library_versions,
                'max_layer': max_layer,
                'min_layer': min_layer,
                'sip_version': sip_version,
                'support_call_out': support_call_out,
                'user_guid': user_guid
            }
        )