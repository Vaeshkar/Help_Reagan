from setuptools import setup

APP = ['help_reagan.py']
DATA_FILES = ['assets', 'sounds']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'assets/app.icns',
    'includes': ['pygame'],
    'resources': ['assets', 'sounds']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)