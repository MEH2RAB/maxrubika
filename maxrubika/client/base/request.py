from typing import Union, Optional, Dict
from ..core.cipher import Cipher
from ...data import Data
from .. import exceptions
import maxrubika
import asyncio

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
            self.key = Cipher.passphrase(self.auth)

        client = self.DEFAULT_PLATFORM.copy()

        data = {"api_version": self.API_VERSION}
        data["tmp_session" if tmp_session else "auth"] = (
            self.auth if tmp_session else self.decode_auth
        )

        data_enc = {"client": client, "method": method, "input": input or {}}
        if encrypt:
            data["data_enc"] = Cipher.encrypt(data_enc, key=self.key)
            if not tmp_session:
                data["sign"] = Cipher.sign(self.import_key, data["data_enc"])

        result = await self.connection._http_request(data, max_retries=self.max_retries)

        if result is None:
            return None

        data_enc = result.get('data_enc')
        if data_enc is not None:
            result = Cipher.decrypt(data_enc, key=self.key)

        status = result.get('status')
        status_det = result.get('status_det')

        if status == 'OK' and status_det == 'OK':
            data_result = result.get('data')

            if data_result is None:
                return None

            if isinstance(data_result, dict):
                data_result['_client'] = self

            return Data(data_result)

        exceptions.raise_exception(status_det, result, None)