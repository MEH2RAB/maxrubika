import os
import json
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class UpgradeToApi6:
    async def upgrade_to_api6(
        self: "maxrubika.Messenger",
        save_as: bool = True,
        file_name: Optional[str] = None
    ):
        """
        Upgrade from API v5 to v6 by setting an RSA public key.

        This allows old v5 auth keys to be used with API v6.
        After upgrade, save the returned private_key for future v6 logins.

        Parameters:
            save_as (bool): If True (default), saves auth and private_key to a JSON file.
            file_name (str, optional): Custom file name for the JSON file. Defaults to 'maxrubika_{auth[:10]}'.

        Returns:
            Data: Response with status, message, auth, and private_key.
        """
        from ....data import Data
        from ...exceptions import ApiVersionError
        from ...core.cipher import Cipher
        from Crypto.PublicKey import RSA
        from Crypto.Signature import pkcs1_15

        if self.API_VERSION != 5:
            raise ApiVersionError("This method only works with api_version = 5.")

        public_key, private_key = Cipher.create_keys()

        await self.request(
            method="setPublicKey",
            input={"public_key": public_key}
        )

        self.private_key = private_key
        self.API_VERSION = 6
        self.import_key = pkcs1_15.new(RSA.import_key(self.private_key.encode()))

        if save_as:
            name = file_name if file_name else f"maxrubika_{self.auth[:10]}"
            file_path = os.path.abspath(f"{name}.json")
            with open(file_path, "w") as f:
                json.dump({"auth": self.auth, "private_key": private_key}, f, indent=2)

            result_dict = {
                "status": "OK",
                "message": f"Saved to {file_path}",
                "auth": self.auth,
                "private_key": private_key
            }
        else:
            result_dict = {
                "status": "OK",
                "message": "Please save your private key to avoid issues.",
                "auth": self.auth,
                "private_key": private_key
            }

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)