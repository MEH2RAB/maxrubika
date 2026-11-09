# rubino/crypto.py
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class Crypto:
    IV = b"\x00" * 16

    @staticmethod
    def make_key(auth: str) -> bytes:
        if len(auth) != 32:
            raise ValueError("auth must be exactly 32 characters")

        part1 = auth[:8]
        part2 = auth[8:16]
        part3 = auth[16:24]
        part4 = auth[24:32]

        s = part3 + part1 + part4 + part2

        result = []
        for c in s:
            if "0" <= c <= "9":
                result.append(chr(((ord(c) - ord("0") + 5) % 10) + ord("0")))
            elif "a" <= c <= "z":
                result.append(chr(((ord(c) - ord("a") + 9) % 26) + ord("a")))
            else:
                result.append(c)

        return "".join(result).encode()

    @classmethod
    def encrypt_auth(cls, text: str, auth: str) -> str:
        key = cls.make_key(auth)
        cipher = AES.new(key, AES.MODE_CBC, cls.IV)
        encrypted = cipher.encrypt(pad(text.encode(), AES.block_size))
        return base64.b64encode(encrypted).decode()

    @classmethod
    def decrypt_auth(cls, cipher_b64: str, auth: str) -> str:
        key = cls.make_key(auth)
        cipher = AES.new(key, AES.MODE_CBC, cls.IV)
        decrypted = unpad(cipher.decrypt(base64.b64decode(cipher_b64)), AES.block_size)
        return decrypted.decode()