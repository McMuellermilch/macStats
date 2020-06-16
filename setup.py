from setuptools import setup

APP = ['./src/app.py']
DATA_FILES = ['./resources/app_icon_green.png',
              './resources/app_icon_red.png', './resources/app_icon_white.png']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleShortVersionString': '0.2.0',
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    name='macStats',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps']
)
