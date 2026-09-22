import warnings
import secrets
import re
import uuid
import maxrubika

system_versions = {
    'Windows NT 10.0': 'Windows 10/11',
    'Windows NT 6.2': 'Windows 8',
    'Windows NT 6.1': 'Windows 7',
    'Windows NT 6.0': 'Windows Vista',
    'Windows NT 5.1': 'Windows XP',
    'Windows NT 5.0': 'Windows 2000',
    'Mac': 'Mac/iOS',
    'X11': 'UNIX',
    'Linux': 'Linux',
    'Ubuntu': 'Ubuntu',
    'Fedora': 'Fedora',
    'Debian': 'Debian',
    'Arch Linux': 'Arch Linux',
    'CentOS': 'CentOS',
    'Red Hat': 'Red Hat'
}

def _get_device_info(
    user_agent: str,
    lang_code: str,
    app_version: str,
    platform: str,
    phone_number: str = None,
    custom_device: str = None
) -> dict:

    if custom_device:
        device_model = str(custom_device)

    elif platform == 'Android':
        device_model = 'samsungSM-S938B'

    else:
        device_match = re.search(r'(opera|chrome|safari|firefox|msie|trident|edge)\/(\d+)', user_agent.lower())

        if device_match:
            device_model = (
                f"{device_match.group(1).title()} "
                f"{device_match.group(2)}"
            )
        else:
            device_model = 'Unknown'
            warnings.warn(f'Can not parse user-agent ({user_agent})')

    if platform == 'Android':
        system_version = 'SDK 35'
    else:
        system_version = 'Unknown'

        for key, value in system_versions.items():
            if key in user_agent:
                system_version = value
                break

    if platform == 'Android':
        prefix = 'MA'
    elif platform == 'Web':
        prefix = 'WB'
    else:
        prefix = 'PW'

    if platform == 'Android':
        device_hash = secrets.token_hex(8)
    else:
        device_hash = ('2' + ''.join(re.findall(r'\d+', user_agent)))

    if platform == 'Web':
        token_type = 'Web'
    else:
        token_type = 'Firebase'

    device_info = {
        'token': '',
        'lang_code': lang_code,
        'token_type': token_type,
        'app_version': f'{prefix}_{app_version}',
        'system_version': system_version,
        'device_model': device_model,
        'device_hash': device_hash,
        'phone_number': phone_number,
    }

    if platform == 'Android':
        device_info.update({
            'ads_id': f'GOOGLE_{uuid.uuid4()}',
            'is_multi_account': False
        })
    return device_info

class RegisterDevice:
    async def register_device(
        self: "maxrubika.Client",
        device_model: str = None,
        *args,
        **kwargs
    ):
        """
        Register the current device with the Rubika server.

        Parameters:
            device_model (str, optional):
                Custom device model name.

        Returns:
            The result of the API call.
        """
        platform = self.DEFAULT_PLATFORM['platform']

        app_version = self.DEFAULT_PLATFORM.get('app_version')

        lang_code = self.DEFAULT_PLATFORM.get('lang_code', 'fa')

        info = self.session.information()
        phone_number = info[0]

        device_info = _get_device_info(
            self.user_agent,
            lang_code,
            app_version,
            platform,
            phone_number=phone_number,
            custom_device=device_model
        )

        return await self.request(
            method = 'registerDevice',
            input = device_info
        )