DEFAULT_PLATFORM = {
    'app_name': 'Main',
    'app_version': '2.5.8',
    'platform': 'PWA',
    'package': 'm.rubika.ir',
    'lang_code': 'fa',
}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/150.0.7871.115 Safari/537.36"
)

PLATFORMS = {

    'web': {
        'platform': 'Web',
        'app_version': '4.4.33',
        'package': 'web.rubika.ir',
        'headers': {
            'origin': 'https://web.rubika.ir',
            'referer': 'https://web.rubika.ir/',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'pwa': {
        'platform': 'PWA',
        'app_version': '2.5.8',
        'package': 'm.rubika.ir',
        'headers': {
            'origin': 'https://m.rubika.ir',
            'referer': 'https://m.rubika.ir/',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'android': {
        'platform': 'Android',
        'app_version': '4.1.1',
        'package': 'app.rbmain.a',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'rubx': {
        'platform': 'Android',
        'app_version': '4.1.1',
        'package': 'ir.rubx.bapp',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'rubikids': {
        'platform': 'Android',
        'app_version': '4.1.1',
        'package': 'app.rbmain.kids',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'rubino': {
        'platform': 'Android',
        'app_version': '4.1.1',
        'package': 'app.rubino.main',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },

    'shad_web': {
        'platform': 'Web',
        'app_version': '4.4.26',
        'package': 'web.shad.ir',
        'headers': {
            'origin': 'https://web.shad.ir',
            'referer': 'https://web.shad.ir/',
        },
        'get_dcs_url': 'https://shgetdcmess.iranlms.ir/',
        'storage_prefix': 'shstorage',
    },
    'shad_pwa': {
        'platform': 'PWA',
        'app_version': '3.0.8',
        'package': 'my.shad.ir',
        'headers': {
            'origin': 'https://my.shad.ir',
            'referer': 'https://my.shad.ir/',
        },
        'get_dcs_url': 'https://shgetdcmess.iranlms.ir/',
        'storage_prefix': 'shstorage',
    },
    'shad_android': {
        'platform': 'Android',
        'app_version': '3.8.0',
        'package': 'ir.medu.shad',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
        'get_dcs_url': 'https://shgetdcmess.iranlms.ir/',
        'storage_prefix': 'shstorage',
    },
}

RUBIKA_PLATFORM_NAMES = ['Web', 'PWA', 'Android', 'RubX', 'RubiKids', 'Rubino']

RUBIKA_PLATFORM_ALIASES = {
    'rubx': 'RubX',
    'rubikids': 'RubiKids',
    'rubino': 'Rubino',
}

SHAD_PLATFORM_NAMES = ['ShadWeb', 'ShadPWA', 'ShadAndroid']

SHAD_PLATFORM_ALIASES = {
    'shad_web': 'ShadWeb',
    'shad_pwa': 'ShadPWA',
    'shad_android': 'ShadAndroid',
}

PLATFORM_NAME_TO_KEY = {
    'Web': 'web',
    'PWA': 'pwa',
    'Android': 'android',
    'RubX': 'rubx',
    'RubiKids': 'rubikids',
    'Rubino': 'rubino',
    'ShadWeb': 'shad_web',
    'ShadPWA': 'shad_pwa',
    'ShadAndroid': 'shad_android',
}

VALID_PLATFORMS = list(PLATFORMS.keys())