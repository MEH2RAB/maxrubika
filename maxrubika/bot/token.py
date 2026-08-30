import os
import json
import zlib
import base64
import secrets
from hashlib import sha256, sha512, pbkdf2_hmac
from Crypto.Cipher import AES

class TokenString:
    _SECRET_PASSWORD = b"MAXRubika_Bot_Ultra_Secret_1405"
    _ROUNDS = 3

    def __init__(self, string: str = ""):
        self._string = string

    @classmethod
    def _derive_master_key(cls, salt: bytes, password: str = None) -> bytes:
        if password:
            return pbkdf2_hmac('sha256', password.encode(), salt, 300000, dklen=32)
        return pbkdf2_hmac('sha256', cls._SECRET_PASSWORD, salt, 300000, dklen=32)

    @classmethod
    def _xor(cls, data: bytes, key: bytes) -> bytes:
        return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

    @classmethod
    def _encrypt_layer(cls, data: bytes, key: bytes) -> bytes:
        nonce = secrets.token_bytes(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        ciphertext = cls._xor(ciphertext, sha512(key + nonce).digest())
        return nonce + tag + ciphertext

    @classmethod
    def _decrypt_layer(cls, data: bytes, key: bytes) -> bytes:
        nonce = data[:12]
        tag = data[12:28]
        ciphertext = cls._xor(data[28:], sha512(key + nonce).digest())
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)

    @classmethod
    def from_token(cls, token: str, password: str = None) -> "TokenString":
        json_str = json.dumps({"token": token}, separators=(',', ':'))
        compressed = zlib.compress(json_str.encode(), level=9)
        combined = sha512(compressed).digest() + compressed

        for _ in range(cls._ROUNDS):
            salt = secrets.token_bytes(16)
            key = cls._derive_master_key(salt, password)
            combined = salt + cls._encrypt_layer(combined, key)

        return cls(base64.b64encode(combined).decode())

    def to_token(self, password: str = None) -> str:
        if not self._string:
            return ""

        try:
            combined = base64.b64decode(self._string.encode())

            for _ in range(self._ROUNDS):
                key = self._derive_master_key(combined[:16], password)
                combined = self._decrypt_layer(combined[16:], key)

            data_hash, compressed = combined[:64], combined[64:]
            if sha512(compressed).digest() != data_hash:
                raise ValueError("Hash mismatch.")

            data = json.loads(zlib.decompress(compressed).decode())
            return data.get('token', '')
        except Exception:
            return ""

    def __str__(self):
        return self._string

    def __bool__(self):
        return bool(self._string)