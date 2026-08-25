import os
import re
import asyncio
from ..core.cipher import Cipher
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import maxrubika
from ..exceptions import (
    InvalidInput,
    NotRegistered,
    InvalidAccess
)
from ..core.configs import (
    PLATFORMS,
    RUBIKA_PLATFORM_NAMES,
    RUBIKA_PLATFORM_ALIASES,
    SHAD_PLATFORM_NAMES,
    SHAD_PLATFORM_ALIASES,
    PLATFORM_NAME_TO_KEY,
)
from rich.console import Console
from rich.text import Text

console = Console()

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

        if self._original_platform in SHAD_PLATFORM_ALIASES:

            platform_names = SHAD_PLATFORM_NAMES
            current_name = SHAD_PLATFORM_ALIASES[self._original_platform]
        else:
            platform_names = RUBIKA_PLATFORM_NAMES
            if self._original_platform in RUBIKA_PLATFORM_ALIASES:
                current_name = RUBIKA_PLATFORM_ALIASES[self._original_platform]
            else:
                current_name = current_platform

        tried_platforms = [current_name]
        for p in platform_names:
            if p not in tried_platforms:
                tried_platforms.append(p)

        try:
            if self.auth is None or self.private_key is None:
                raise NotRegistered

            self.decode_auth = Cipher.decode_auth(self.auth)
            self.import_key = pkcs1_15.new(RSA.import_key(self.private_key.encode()))

            for platform in tried_platforms:
                if platform != self.DEFAULT_PLATFORM['platform']:
                    config_key = PLATFORM_NAME_TO_KEY.get(platform, platform.lower())
                    
                    config = PLATFORMS.get(config_key, {})
                    self.DEFAULT_PLATFORM['platform'] = config.get('platform', platform)
                    self.DEFAULT_PLATFORM['app_version'] = config.get('app_version', '4.4.33')
                    self.DEFAULT_PLATFORM['package'] = config.get('package', 'web.rubika.ir')

                    if hasattr(self, 'connection'):
                        platform_config = config.get('headers', {})
                        if self.DEFAULT_PLATFORM['platform'] == "Android":
                            self.connection.headers.pop("origin", None)
                            self.connection.headers.pop("referer", None)
                        self.connection.headers.update(platform_config)

                try:
                    result = await self.get_me()
                    self.guid = result.user.user_guid
                    self.logger.info('user', extra={'guid': result})
                    return self

                except (InvalidInput, InvalidAccess, NotRegistered):
                    continue

            raise NotRegistered

        except (InvalidInput, InvalidAccess, NotRegistered):
            if not self.continue_on_error:
                        raise
            config = PLATFORMS.get(self._original_platform, {})
            self.DEFAULT_PLATFORM['platform'] = current_platform
            self.DEFAULT_PLATFORM['app_version'] = config.get('app_version', '4.4.33')
            self.DEFAULT_PLATFORM['package'] = config.get('package', 'web.rubika.ir')

        while True:
            if phone_number is None:
                phone_text = Text()
                phone_text.append("Enter phone number (e.g., +989123456789): ", style="cyan")
                console.print(phone_text, end='')
                phone_number = input()

            phone_number = normalize_phone_number(phone_number)
            if phone_number is None:
                phone_number = None
                continue
            
            phone_number = f'98{phone_number[1:]}' if phone_number.startswith('09') else phone_number

            is_phone_number_true = True
            while is_phone_number_true:
                confirm_text = Text()
                confirm_text.append("\nIs the ", style="cyan")
                confirm_text.append(phone_number, style="bold yellow")
                confirm_text.append(" correct? (y/n): ", style="cyan")
                console.print(confirm_text, end='')
                if input().lower() == 'y':
                    is_phone_number_true = False
                else:
                    retry_text = Text()
                    retry_text.append("\nEnter phone number (e.g., +989123456789): ", style="cyan")
                    console.print(retry_text, end='')
                    phone_number = input()
                    phone_number = normalize_phone_number(phone_number)
                    if phone_number is None:
                        phone_number = None
                        break
                    phone_number = f'98{phone_number[1:]}' if phone_number.startswith('09') else phone_number
            
            if phone_number is None:
                continue

            try:
                result = await self.send_code(phone_number=phone_number)
                break
            except InvalidInput:
                console.print("\nInvalid phone number! Please enter a valid number.\n", style="bright_red")
                phone_number = None

        saved_phone_code_hash = None

        if result.status == 'SendPassKey':
            while True:
                hint = getattr(result, 'hint_pass_key', None)
                if hint:
                    pass_text = Text()
                    pass_text.append("\nEnter 2-step verification password (hint: ", style="cyan")
                    pass_text.append(hint, style="bold yellow")
                    pass_text.append("): ", style="cyan")
                    console.print(pass_text, end='')
                else:
                    pass_text = Text()
                    pass_text.append("\nEnter 2-step verification password: ", style="cyan")
                    console.print(pass_text, end='')
                pass_key = input()
                
                if not pass_key:
                    console.print("\nPassword cannot be empty!", style="bright_red")
                    continue

                result = await self.send_code(phone_number=phone_number, pass_key=pass_key)

                if result.status == 'InvalidPassKey':
                    console.print("\nIncorrect password! Try again.", style="bright_red")
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
                    code_text = Text()
                    if result.send_type == 'SMS':
                        code_text.append("\nVerification code has been sent to you via ", style="cyan")
                        code_text.append("SMS", style="bold yellow")
                        code_text.append(", please enter the code: ", style="cyan")
                    elif result.send_type == 'Internal':
                        code_text.append("\nVerification code has been sent to you via ", style="cyan")
                        code_text.append("'Login Notifications'", style="bold yellow")
                        code_text.append(" service, please check your account and enter the code: ", style="cyan")
                    elif result.send_type == 'CallCode':
                        code_text.append("\nVerification code will be announced to you via a ", style="cyan")
                        code_text.append("phone call", style="bold yellow")
                        code_text.append(", please answer that call and enter the code: ", style="cyan")
                    else:
                        code_text.append("\nVerification code sent via ", style="cyan")
                        code_text.append(result.send_type, style="bold yellow")
                        code_text.append(", please enter the code: ", style="cyan")
                    console.print(code_text, end='')
                else:
                    code_text = Text()
                    code_text.append("\nPlease enter the verification code: ", style="cyan")
                    console.print(code_text, end='')
                first_prompt = False
            else:
                error_text = Text()
                error_text.append("\nCode is incorrect, please enter correct code: ", style="bright_red")
                console.print(error_text, end='')
            
            phone_code = input()

            if not phone_code or not phone_code.strip():
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

                session_path = os.path.abspath(f"{self.session_name}.max")
                session_text = Text()
                session_text.append("\nSession saved to ", style="green")
                session_text.append(session_path, style="bold green")
                session_text.append("\n")
                console.print(session_text)

                await self.register_device(device_model=self.session_name)
                await asyncio.sleep(2)
                return self

            elif result.status == 'CodeIsInvalid':
                continue

            else:
                error_text = Text()
                error_text.append("\nSign in failed: ", style="bold bright_red")
                error_text.append(str(result.status), style="red")
                console.print(error_text)
                break

        return self