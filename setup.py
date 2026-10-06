from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

requirements = ['aiohttp', 'aiofiles', 'mutagen', 'pycryptodome', 'rich']

setup(
    name = 'maxrubika',
    version = '1.16.0',
    author = 'MEHRAB Farahmand',
    author_email = 'MEH2RABx@gmail.com',
    description = 'Python async library for Rubika and Shad Platforms - Build bots and userbots effortlessly.',
    keywords = ['maxrubika', 'rubika', 'bot', 'robot', 'asyncio', 'client', 'shad', 'userbot', 'self-bot'],
    long_description = long_description,
    python_requires = '>=3.8',
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/MEH2RAB/maxrubika',
    project_urls={
        "Documentation": "https://MAXRubi.ir/documents",
        "Source": "https://github.com/MEH2RAB/maxrubika",
        "Channel": "https://rubika.ir/TheMAXRubika",
    },
    packages = find_packages(),
    exclude_package_data = {'': ['*.pyc', '*__pycache__*']},
    install_requires = requirements,
    extras_require = {
        'opencv': ['opencv-python'],
        'movie': ['numpy', 'moviepy'],
        'pillow': ['pillow==9.4.0'],
        'aiortc': ['aiortc'],
        'pro': ['aiortc', 'pillow', 'opencv-python', 'numpy', 'moviepy']
    },
    classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)