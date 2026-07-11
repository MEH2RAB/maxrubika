import re
import warnings
from random import choices
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

def _get_device_info(user_agent: str, lang_code: str, app_version: str, platform: str, custom_device: str = None) -> dict:
    if custom_device:
        device_model = str(custom_device)
    elif platform == 'Android':
        device_model = 'samsungSM-S938B'
    else:
        device_model = re.search(
            r'(opera|chrome|safari|firefox|msie|trident|edge)\/(\d+)',
            user_agent.lower()
        )
        if device_model:
            device_model = f"{device_model.group(1).title()} {device_model.group(2)}"
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
        device_hash = ''.join(choices('0123456789', k=26))
    else:
        device_hash = '2' + ''.join(re.findall(r'\d+', user_agent))

    if platform == 'Web':
        token_type = 'Web'
    else:
        token_type = 'Firebase'

    return {
        'token': '',
        'lang_code': lang_code,
        'token_type': token_type,
        'app_version': f'{prefix}_{app_version}',
        'system_version': system_version,
        'device_model': device_model,
        'device_hash': device_hash,
    }

class RegisterDevice:
    async def register_device(self: "maxrubika.Client", device_model: str = None, *args, **kwargs):
        """
        Register the current device with the Rubika server.

        This method sends device information (model, OS, app version, etc.)
        to the server to register the current session as an active device.

        Parameters:
            device_model (str, optional): Custom device model name.
                If not provided, it will be auto-detected from the User-Agent.

        Returns:
            The result of the API call.
        """
        platform = self.DEFAULT_PLATFORM['platform']
        app_version = self.DEFAULT_PLATFORM.get('app_version')
        lang_code = self.DEFAULT_PLATFORM.get('lang_code', 'fa')

        device_info = _get_device_info(
            self.user_agent,
            lang_code,
            app_version,
            platform,
            custom_device=device_model
        )

        return await self.request(
            method = 'registerDevice',
            input = device_info
        )