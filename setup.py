from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

requirements = ['aiohttp', 'aiofiles', 'mutagen', 'pycryptodome', 'rich']

setup(
    name = 'maxrubika',
    version = '1.3.0',
    author = 'MEHRAB Farahmand',
    author_email = 'MEH2RABx@gmail.com',
    description = 'Python async library for Rubika Messenger - Build bots and userbots effortlessly.',
    keywords = ['maxrubika', 'rubika', 'bot', 'robot', 'asyncio', 'client'],
    long_description = long_description,
    python_requires = '>=3.8',
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/MEH2RAB/maxrubika',
    project_urls={
        "Documentation": "https://maxrubi.ir",
        "Source": "https://github.com/MEH2RAB/maxrubika",
        "Channel": "https://rubika.ir/MAXRubikaLibrary",
    },
    packages = find_packages(),
    exclude_package_data = {'': ['*.pyc', '*__pycache__*']},
    install_requires = requirements,
    extras_require = {
        'cv': ['opencv-python'],
        'movie': ['numpy', 'moviepy', 'pillow'],
        'pil': ['pillow'],
        'rtc': ['aiortc']
    },
    classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)