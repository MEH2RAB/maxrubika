from datetime import datetime

LIVE_VERSION = datetime.now().strftime("%y.%m.%d")

DEFAULT_PLATFORM = {
    'app_name': 'Main',
    'app_version': LIVE_VERSION,
    'platform': 'PWA',
    'package': 'm.rubika.ir',
    'lang_code': 'fa'
}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/150.0.7871.115 Safari/537.36"
)

PLATFORMS = {
    'web': {
        'platform': 'Web',
        'app_version': LIVE_VERSION,
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
        'app_version': LIVE_VERSION,
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
        'app_version': LIVE_VERSION,
        'package': 'app.rbmain.a',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'ios': {
        'platform': 'IOS',
        'app_version': LIVE_VERSION,
        'package': 'com.roobika.xstores',
        'headers': {
            'user-agent': 'Rubika/4.1.1 (iPhone; iOS 17.5.1; Scale/3.00)',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'rubx': {
        'platform': 'Android',
        'app_version': LIVE_VERSION,
        'package': 'ir.rubx.bapp',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'rubikids': {
        'platform': 'Android',
        'app_version': LIVE_VERSION,
        'package': 'app.rbmain.kids',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'rubino': {
        'platform': 'Android',
        'app_version': LIVE_VERSION,
        'package': 'app.rubino.main',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'tv_android': {
        'platform': 'TVAndroid',
        'app_version': LIVE_VERSION,
        'package': 'app.rbmain.tv',
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'tv_web': {
        'platform': 'TVWeb',
        'app_version': LIVE_VERSION,
        'package': 'tv.rubika.ir',
        'headers': {
            'origin': 'https://tv.rubika.ir',
            'referer': 'https://tv.rubika.ir/',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'vod_web': {
        'platform': 'VODWeb',
        'app_version': LIVE_VERSION,
        'package': 'vod.rubika.ir',
        'headers': {
            'origin': 'https://vod.rubika.ir',
            'referer': 'https://vod.rubika.ir/',
        },
        'get_dcs_url': 'https://getdcmess.iranlms.ir/',
        'storage_prefix': 'messenger',
    },
    'shad_web': {
        'platform': 'Web',
        'app_version': LIVE_VERSION,
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
        'app_version': LIVE_VERSION,
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
        'app_version': LIVE_VERSION,
        'package': 'ir.medu.shad',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
        'get_dcs_url': 'https://shgetdcmess.iranlms.ir/',
        'storage_prefix': 'shstorage',
    },
}

RUBIKA_PLATFORM_NAMES = [
    'Web', 'PWA', 'Android', 'IOS', 'RubX', 'RubiKids',
    'Rubino', 'TVAndroid', 'TVWeb', 'VODWeb'
]

RUBIKA_PLATFORM_ALIASES = {
    'rubx': 'RubX',
    'rubikids': 'RubiKids',
    'rubino': 'Rubino',
    'tv_android': 'TVAndroid',
    'tv_web': 'TVWeb',
    'vod_web': 'VODWeb',
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
    'IOS': 'ios',
    'RubX': 'rubx',
    'RubiKids': 'rubikids',
    'Rubino': 'rubino',
    'ShadWeb': 'shad_web',
    'ShadPWA': 'shad_pwa',
    'ShadAndroid': 'shad_android',
    'TVAndroid': 'tv_android',
    'TVWeb': 'tv_web',
    'VODWeb': 'vod_web',
}

VALID_PLATFORMS = list(PLATFORMS.keys())