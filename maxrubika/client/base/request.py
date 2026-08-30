from typing import Union, Optional, Dict
from ..core.cipher import Cipher
from ...data import Data
from .. import exceptions
import maxrubika
import asyncio
import json

class Request:
    async def request(
        self: "maxrubika.Client",
        method: str,
        input: Optional[Dict] = None,
        tmp_session: bool = False,
        encrypt: bool = True
    ):
        """
        Build and send a request to the Rubika API.

        Parameters:
            method (str): API method name (e.g., 'sendMessage', 'getUserInfo').
            input (dict, optional): Input data for the method.
            tmp_session (bool): Use temporary session instead of auth (default: False).
            encrypt (bool): Encrypt the request data (default: True).

        Returns:
            Data or None: The API response.
        """
        if not hasattr(self, 'connection') or self.connection is None:
            await self.connect()

        if not self.connection.api_url:
            await self.connection.get_dcs(max_retries=self.max_retries)

        if self.auth is None:
            self.auth = Cipher.secret(length=32)

        if self.key is None:
            if self.API_VERSION == 5:
                self.key = Cipher.secret_v5(self.auth)
            else:
                self.key = Cipher.passphrase(self.auth)

        client = self.DEFAULT_PLATFORM.copy()

        data = {"api_version": str(self.API_VERSION)}

        if self.API_VERSION == 5:
            if tmp_session:
                data["tmp_session"] = self.auth
            else:
                data["auth"] = self.auth
        else:
            data["tmp_session" if tmp_session else "auth"] = (
                self.auth if tmp_session else self.decode_auth
            )

        data_enc = {"method": method, "input": input or {}, "client": client}

        if encrypt:
            if self.API_VERSION == 5:
                data["data_enc"] = Cipher.encrypt_v5(
                    json.dumps(data_enc), key=self.key
                )
            else:
                data["data_enc"] = Cipher.encrypt(data_enc, key=self.key)
                if not tmp_session:
                    data["sign"] = Cipher.sign(self.import_key, data["data_enc"])

        result = await self.connection._http_request(data, max_retries=self.max_retries)

        if result is None:
            return None

        data_enc = result.get('data_enc')
        if data_enc is not None:
            if self.API_VERSION == 5:
                result = Cipher.decrypt_v5(data_enc, key=self.key)
            else:
                result = Cipher.decrypt(data_enc, key=self.key)

        status = result.get('status')
        status_det = result.get('status_det')

        if status == 'OK' and status_det == 'OK':
            data_result = result.get('data')

            if data_result is None:
                return Data({})

            if isinstance(data_result, dict):
                data_result['_client'] = self

            return Data(data_result)

        exceptions.raise_exception(status_det, result, None)