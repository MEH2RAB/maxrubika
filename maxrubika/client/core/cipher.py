import re
import json
import base64
import string
import secrets
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from string import ascii_lowercase, ascii_uppercase

class Cipher:
    AES_IV = b"\x00" * 16

    @staticmethod
    def decode_auth(auth: str) -> str:
        result_list, digits = [], "0123456789"
        translation_table_lower = str.maketrans(
            ascii_lowercase,
            "".join([chr(((32 - (ord(c) - 97)) % 26) + 97) for c in ascii_lowercase]),
        )
        translation_table_upper = str.maketrans(
            ascii_uppercase,
            "".join([chr(((29 - (ord(c) - 65)) % 26) + 65) for c in ascii_uppercase]),
        )

        for char in auth:
            if char in ascii_lowercase:
                result_list.append(char.translate(translation_table_lower))
            elif char in ascii_uppercase:
                result_list.append(char.translate(translation_table_upper))
            elif char in digits:
                result_list.append(chr(((13 - (ord(char) - 48)) % 10) + 48))
            else:
                result_list.append(char)

        return "".join(result_list)

    @classmethod
    def passphrase(cls, auth):
        if len(auth) != 32:
            raise ValueError("auth length should be 32 digits")

        result_list = []
        chunks = re.findall(r"\S{8}", auth)
        for character in chunks[2] + chunks[0] + chunks[3] + chunks[1]:
            result_list.append(chr(((ord(character) - 97 + 9) % 26) + 97))
        return "".join(result_list)

    @classmethod
    def secret(cls, length):
        return "".join(secrets.choice(string.ascii_lowercase) for _ in range(length))

    @classmethod
    def decrypt(cls, data, key):
        aes = AES.new(key.encode(), AES.MODE_CBC, cls.AES_IV)
        dec = aes.decrypt(base64.urlsafe_b64decode(data.encode("UTF-8")))
        dec_res = unpad(dec, AES.block_size).decode("UTF-8")

        dec_res = re.sub(r'"time":,', '"time":0,', dec_res)
        dec_res = re.sub(r'"size":,', '"size":0,', dec_res)
        
        return json.loads(dec_res)

    @classmethod
    def encrypt(cls, data: str, key: str):
        if isinstance(data, dict):
            data = json.dumps(data)
        raw = pad(data.encode("UTF-8"), AES.block_size)
        aes = AES.new(key.encode(), AES.MODE_CBC, cls.AES_IV)
        return base64.b64encode(aes.encrypt(raw)).decode("UTF-8")

    @staticmethod
    def sign(pkcs1_15_obj: "pkcs1_15.new", data: str) -> str:
        signature = pkcs1_15_obj.sign(SHA256.new(data.encode("utf-8")))
        return base64.b64encode(signature).decode("utf-8")

    @staticmethod
    def create_keys() -> tuple:
        keys = RSA.generate(2048)
        public_key = Cipher.decode_auth(
            base64.b64encode(keys.publickey().export_key()).decode("utf-8")
        )
        private_key = keys.export_key().decode("utf-8")
        return public_key, private_key

    @staticmethod
    def decrypt_RSA_OAEP(private_key: str, data: str):
        key = RSA.import_key(private_key.encode("utf-8"))
        return PKCS1_OAEP.new(key).decrypt(base64.b64decode(data)).decode("utf-8")