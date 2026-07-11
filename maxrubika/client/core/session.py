import os
import json
import sqlite3
from hashlib import sha256
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

class Session:
    def __init__(self, session: str, create_file: bool = False) -> None:
        self.filename = session
        if not session.endswith(suffix):
            self.filename += suffix

        self.create_file = create_file
        self._connection = None
        self._cursor = None
        self.is_logged_in = False
        self._imported_from = None

        if os.path.exists(self.filename) and not self.create_file:
            try:
                self._initialize_connection()
                info = self.information()
                if info and info[0]:
                    self.is_logged_in = True
                else:
                    self.close()
                    os.remove(self.filename)
                    self._connection = None
                    self._cursor = None
            except Exception:
                self.close()
                try:
                    os.remove(self.filename)
                except:
                    pass
                self._connection = None
                self._cursor = None

        elif not self.create_file:
            base_name = self.filename.replace('.max', '')
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

        elif self.create_file:
            self._initialize_database()

    def _initialize_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self.filename, check_same_thread=False)
            self._cursor = self._connection.cursor()

    def _initialize_database(self):
        self._initialize_connection()
        self._cursor.execute('DROP TABLE IF EXISTS session')
        self._cursor.execute('CREATE TABLE IF NOT EXISTS session (data BLOB)')
        self._connection.commit()

    def information(self):
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
                    data.get('phone'),
                    data.get('auth'),
                    data.get('guid'),
                    data.get('agent'),
                    data.get('private_key')
                )

            return None

        except Exception:
            return None

    def insert(self, phone_number, auth, guid, user_agent, private_key,
               *args, **kwargs):
        if self._connection is None:
            self.create_file = True
            self._initialize_database()

        self._cursor.execute("PRAGMA table_info(session)")
        columns = [col[1] for col in self._cursor.fetchall()]
        if 'data' not in columns:
            self._cursor.execute('DROP TABLE IF EXISTS session')
            self._cursor.execute('CREATE TABLE session (data BLOB)')
            self._connection.commit()

        data = {
            'phone': phone_number,
            'auth': auth,
            'guid': guid,
            'agent': user_agent,
            'private_key': private_key
        }

        encrypted = _encrypt(data)

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
        self.close()