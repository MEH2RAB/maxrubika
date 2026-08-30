import os
import json
import zlib
import base64
import sqlite3
import secrets
from hashlib import sha256, sha512, pbkdf2_hmac
from Crypto.Cipher import AES

suffix = '.max'
_DB_KEY = sha256(b'maxrubika_session_full_encrypt_v2').digest()

def _encrypt(data: dict) -> bytes:
    plaintext = json.dumps(data).encode('utf-8')
    nonce = os.urandom(12)
    cipher = AES.new(_DB_KEY, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return nonce + tag + ciphertext

def _decrypt(data: bytes) -> dict:
    nonce = data[:12]
    tag = data[12:28]
    ciphertext = data[28:]
    cipher = AES.new(_DB_KEY, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return json.loads(plaintext.decode('utf-8'))

def _read_rp_session(filename: str):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute('SELECT phone, auth, guid, agent, private_key FROM session')
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'phone': result[0],
            'auth': result[1],
            'guid': result[2],
            'agent': result[3],
            'private_key': result[4]
        }
    return None

def _read_json_session(filename: str):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        user = data.get('user', {})
        return {
            'phone': user.get('phone', ''),
            'auth': data.get('auth', '') or data.get('Auth', ''),
            'guid': user.get('user_guid', '') or data.get('guid', ''),
            'agent': user.get('user_agent', 'Mozilla/5.0') or data.get('agent', 'Mozilla/5.0'),
            'private_key': data.get('private_key', '') or data.get('Key', '')
        }
    except:
        return None

def _find_session(filename_without_ext: str):
    for ext in ['.max', '.rp', '.pyrubi', '.rubka', '.json']:
        full_path = filename_without_ext + ext
        if os.path.exists(full_path):
            if ext == '.max':
                try:
                    conn = sqlite3.connect(full_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT data FROM session')
                    row = cursor.fetchone()
                    conn.close()
                    if row and row[0]:
                        return _decrypt(row[0]), ext
                except:
                    pass
            elif ext == '.rp':
                data = _read_rp_session(full_path)
                if data:
                    return data, ext
            elif ext in ('.pyrubi', '.rubka', '.json'):
                data = _read_json_session(full_path)
                if data and data.get('auth'):
                    return data, ext
    return None, None

class StringSession:
    _SECRET_PASSWORD = b"MAXRubika_Ultra_Secret_2026"
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
    def from_data(cls, data: dict, password: str = None) -> "StringSession":

        json_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        compressed = zlib.compress(json_str.encode(), level=9)
        combined = sha512(compressed).digest() + compressed

        for _ in range(cls._ROUNDS):
            salt = secrets.token_bytes(16)
            key = cls._derive_master_key(salt, password)
            combined = salt + cls._encrypt_layer(combined, key)

        return cls(base64.b64encode(combined).decode())

    def to_data(self, password: str = None) -> dict:
        if not self._string:
            return {}

        try:
            combined = base64.b64decode(self._string.encode())

            for _ in range(self._ROUNDS):
                key = self._derive_master_key(combined[:16], password)
                combined = self._decrypt_layer(combined[16:], key)

            data_hash, compressed = combined[:64], combined[64:]
            if sha512(compressed).digest() != data_hash:
                raise ValueError("Hash mismatch.")

            return json.loads(zlib.decompress(compressed).decode())
        except Exception:
            return {}

    def __str__(self):
        return self._string

    def __bool__(self):
        return bool(self._string)

class Session:
    def __init__(self, session: str = None, create_file: bool = False,
                 string_session: str = None, password: str = None) -> None:

        self._connection = None
        self._cursor = None
        self._data = None
        self.is_logged_in = False
        self._imported_from = None

        if string_session:
            data = StringSession(string_session).to_data(password)
            if not data:
                raise ValueError("Invalid StringSession or wrong password.")
            self.filename = None
            self.create_file = False
            self._imported_from = "string_session"
            self._data = data
            self.is_logged_in = True
            return

        self.filename = session if session and session.endswith(suffix) else f"{session}{suffix}"
        self.create_file = create_file

        if os.path.exists(self.filename) and not create_file:
            self._initialize_connection()
            info = self.information()
            if info and info[0]:
                self.is_logged_in = True
            else:
                self.close()
                os.remove(self.filename)
                self._connection = None
                self._cursor = None

        elif not create_file:
            base_name = self.filename.replace(suffix, '')
            imported_data, ext = _find_session(base_name)
            if imported_data:
                self._imported_from = base_name + ext
                self._initialize_database()
                self.insert(
                    imported_data.get('phone'),
                    imported_data.get('auth'),
                    imported_data.get('guid'),
                    imported_data.get('agent'),
                    imported_data.get('private_key')
                )
                self.is_logged_in = True

        elif create_file:
            self._initialize_database()

    def _initialize_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self.filename, check_same_thread=False)
            self._cursor = self._connection.cursor()

    def _initialize_database(self):
        self._initialize_connection()
        self._cursor.execute('DROP TABLE IF EXISTS session')
        self._cursor.execute('CREATE TABLE session (data BLOB)')
        self._connection.commit()

    def information(self):
        if self._data is not None:
            return (
                self._data.get('phone'),
                self._data.get('auth'),
                self._data.get('guid'),
                self._data.get('agent', 'Mozilla/5.0'),
                self._data.get('private_key')
            )

        if not self._connection:
            return None

        try:
            cursor = self._connection.cursor()
            cursor.execute('SELECT data FROM session')
            result = cursor.fetchone()
            cursor.close()
            if result and result[0] is not None:
                data = _decrypt(result[0])
                return (
                    data.get('phone'), data.get('auth'), data.get('guid'),
                    data.get('agent'), data.get('private_key')
                )
        except Exception:
            pass
        return None

    def insert(self, phone_number, auth, guid, user_agent, private_key,
               *args, **kwargs):
        if self._data is not None:
            self._data = {
                'phone': phone_number, 'auth': auth, 'guid': guid,
                'agent': user_agent, 'private_key': private_key
            }
            self.is_logged_in = True
            return

        if self._connection is None:
            self._initialize_database()

        encrypted = _encrypt({
            'phone': phone_number, 'auth': auth, 'guid': guid,
            'agent': user_agent, 'private_key': private_key
        })

        cursor = self._connection.cursor()
        cursor.execute('DELETE FROM session')
        cursor.execute('INSERT INTO session VALUES (?)', (encrypted,))
        self._connection.commit()
        cursor.close()
        self.is_logged_in = True

    @classmethod
    def from_string(cls, session_obj, file_name=None):
        info = session_obj.information()
        if file_name is None:
            if info is None or not info[0]:
                raise ValueError('file_name arg is not set')
            file_name = info[0]
        session_instance = cls(file_name, create_file=(info is None))
        if info is not None:
            session_instance.insert(*info)
        return session_instance

    def close(self):
        if self._connection:
            self._connection.commit()
            self._connection.close()
            self._connection = None
            self._cursor = None
            self.is_logged_in = False

    def __del__(self):
        try:
            self.close()
        except:
            pass