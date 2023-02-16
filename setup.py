from setuptools import setup

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    name="bustracker",
    version="0.0.1",
    install_requires=[
        'certifi',
        'charset-normalizer',
        'click',
        'dominate',
        'Flask',
        'Flask-Bootstrap',
        'Flask-WTF',
        'Flask-SQLAlchemy',
        'gtfs-realtime-bindings',
        'idna',
        'importlib-metadata',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'protobuf',
        'requests',
        'urllib3',
        'visitor',
        'Werkzeug',
        'WTForms',
        'zipp',
    ],
)
