# ftp_cli/setup.py

from setuptools import setup

setup(
    name='ftp-cli',
    version='1.0',
    py_modules=['main'],
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'ftp-cli = main:main',
        ],
    },
)
