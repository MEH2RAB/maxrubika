import re
from ..core.cipher import Cipher
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import maxrubika
from ..exceptions import (
    InvalidInput,
    NotRegistered,
    InvalidAccess,
    TooRequests
)

def convert_farsi_digits(text):
    return text.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))

def normalize_phone_number(phone: str) -> str:
    phone = convert_farsi_digits(phone)
    phone = phone.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    pattern = re.compile(r"^(?:\+|00)?(\d{7,15})$")
    match = pattern.match(phone)

    if match:
        return match.group(1) if phone.startswith("00") else f"{match.group(1)}"
    return None

class Start:
    async def start(self: "maxrubika.Client", phone_number: str = None):
        """
        Start the client, handling authentication and registration.

        Parameters:
            phone_number (str, optional): Phone number for registration.

        Returns:
            Client: The initialized client instance.
        """
        if not hasattr(self, 'connection'):
            await self.connect()

        current_platform = self.DEFAULT_PLATFORM['platform']

        all_platforms = ['Web', 'PWA', 'Android']
        tried_platforms = [current_platform]
        for p in all_platforms:
            if p not in tried_platforms:
                tried_platforms.append(p)

        try:
            if self.auth is None or self.private_key is None:
                raise NotRegistered

            self.decode_auth = Cipher.decode_auth(self.auth)
            self.import_key = pkcs1_15.new(RSA.import_key(self.private_key.encode()))

            for platform in tried_platforms:
                if platform != self.DEFAULT_PLATFORM['platform']:
                    self.DEFAULT_PLATFORM['platform'] = platform
                    if platform == 'Web':
                        self.DEFAULT_PLATFORM['app_version'] = '4.4.33'
                        self.DEFAULT_PLATFORM['package'] = 'web.rubika.ir'
                    elif platform == 'Android':
                        self.DEFAULT_PLATFORM['app_version'] = '4.0.5'
                        self.DEFAULT_PLATFORM['package'] = 'app.rbmain.a'
                    else:
                        self.DEFAULT_PLATFORM['app_version'] = '2.5.8'
                        self.DEFAULT_PLATFORM['package'] = 'm.rubika.ir'

                    if hasattr(self, 'connection'):
                        if platform == "Android":
                            self.connection.headers.pop("origin", None)
                            self.connection.headers.pop("referer", None)
                            self.connection.headers["user-agent"] = "okhttp/3.12.1"
                        elif platform == "Web":
                            self.connection.headers["origin"] = "https://web.rubika.ir"
                            self.connection.headers["referer"] = "https://web.rubika.ir/"
                        else:
                            self.connection.headers["origin"] = "https://m.rubika.ir"
                            self.connection.headers["referer"] = "https://m.rubika.ir/"

                try:
                    result = await self.get_me()
                    self.guid = result.user.user_guid
                    self.logger.info('user', extra={'guid': result})
                    return self

                except (NotRegistered, InvalidInput, InvalidAccess):
                    continue

            raise NotRegistered

        except (NotRegistered, InvalidInput, InvalidAccess):
            self.DEFAULT_PLATFORM['platform'] = current_platform
            if current_platform == 'Web':
                self.DEFAULT_PLATFORM['app_version'] = '4.4.33'
                self.DEFAULT_PLATFORM['package'] = 'web.rubika.ir'
            elif current_platform == 'Android':
                self.DEFAULT_PLATFORM['app_version'] = '4.0.5'
                self.DEFAULT_PLATFORM['package'] = 'app.rbmain.a'
            else:
                self.DEFAULT_PLATFORM['app_version'] = '2.5.8'
                self.DEFAULT_PLATFORM['package'] = 'm.rubika.ir'

        if phone_number is None:
            phone_number = input('Enter phone number (e.g., +989123456789): ')
            is_phone_number_true = True
            while is_phone_number_true:
                if input(f'Is the {phone_number} correct? (y/n): ').lower() == 'y':
                    is_phone_number_true = False
                else:
                    phone_number = input('\nEnter phone number (e.g., +989123456789): ')

        phone_number = normalize_phone_number(phone_number)
        phone_number = f'98{phone_number[1:]}' if phone_number.startswith('09') else phone_number

        result = await self.send_code(phone_number=phone_number)

        saved_phone_code_hash = None

        if result.status == 'SendPassKey':
            while True:
                hint = getattr(result, 'hint_pass_key', None)
                if hint:
                    pass_key = input(f'\nEnter 2-step verification password (hint: {hint}): ')
                else:
                    pass_key = input('\nEnter 2-step verification password: ')
                
                if not pass_key:
                    print("\nPassword cannot be empty!")
                    continue

                result = await self.send_code(phone_number=phone_number, pass_key=pass_key)

                if result.status == 'InvalidPassKey':
                    print("\nIncorrect password! Try again.")
                    continue

                if result.status == 'OK':
                    saved_phone_code_hash = result.phone_code_hash
                    break
                else:
                    print(result)
                    break
        else:
            saved_phone_code_hash = result.phone_code_hash

        if saved_phone_code_hash is None:
            raise InvalidAccess("Failed to get 'phone_code_hash'.")

        public_key, self.private_key = Cipher.create_keys()
        phone_code = None
        first_prompt = True

        while True:
            if first_prompt:
                if hasattr(result, 'send_type') and result.send_type:
                    if result.send_type == 'SMS':
                        phone_code = input("\nVerification code has been sent to you via SMS, please enter the code: ")
                    elif result.send_type == 'Internal':
                        phone_code = input("\nVerification code has been sent to you via 'Login Notifications' service, please check your account and enter the code: ")
                    elif result.send_type == 'CallCode':
                        phone_code = input("\nVerification code will be announced to you via a phone call, please answer that call and enter the code: ")
                    else:
                        phone_code = input(f"\nVerification code sent via {result.send_type}, please enter the code: ")
                else:
                    phone_code = input("\nPlease enter the verification code: ")
                first_prompt = False
            else:
                phone_code = input("\nCode is incorrect, please enter correct code: ")

            if not phone_code or not phone_code.strip():
                print("\nCode cannot be empty! Please enter the code.")
                continue

            result = await self.sign_in(
                phone_code=phone_code,
                phone_number=phone_number,
                phone_code_hash=saved_phone_code_hash,
                public_key=public_key
            )

            if result.status == 'OK':
                result.auth = Cipher.decrypt_RSA_OAEP(self.private_key, result.auth)
                self.key = Cipher.passphrase(result.auth)
                self.auth = result.auth
                self.decode_auth = Cipher.decode_auth(self.auth)
                self.import_key = pkcs1_15.new(RSA.import_key(self.private_key.encode()))

                self.session.insert(
                    auth=self.auth,
                    guid=result.user.user_guid,
                    user_agent=self.user_agent,
                    phone_number=result.user.phone,
                    private_key=self.private_key
                )

                await self.register_device(device_model=self.session_name)
                return self

            elif result.status == 'CodeIsInvalid':
                continue

            else:
                print(f"\nSign in failed: {result.status}")
                break

        return self