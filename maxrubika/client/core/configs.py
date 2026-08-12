DEFAULT_PLATFORM = {
    'app_name': 'Main',
    'app_version': '4.4.33',
    'platform': 'Web',
    'package': 'web.rubika.ir',
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
    },
    'pwa': {
        'platform': 'PWA',
        'app_version': '2.5.8',
        'package': 'm.rubika.ir',
        'headers': {
            'origin': 'https://m.rubika.ir',
            'referer': 'https://m.rubika.ir/',
        },
    },
    'android': {
        'platform': 'Android',
        'app_version': '4.0.5',
        'package': 'app.rbmain.a',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
    },
    'rubx': {
        'platform': 'Android',
        'app_version': '4.0.5',
        'package': 'ir.rubx.bapp',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
    },
    'rubikids': {
        'platform': 'Android',
        'app_version': '4.0.5',
        'package': 'app.rbmain.kids',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
    },
    'rubino': {
        'platform': 'Android',
        'app_version': '4.0.5',
        'package': 'app.rubino.main',
        'headers': {
            'user-agent': 'okhttp/3.12.1',
        },
    },
}

VALID_PLATFORMS = list(PLATFORMS.keys())