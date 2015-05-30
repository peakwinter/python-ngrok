#!/usr/bin/env python

from distutils.core import setup

setup(
    name='python-ngrok',
    version='0.1',
    description='Python bindings for ngrok local and Link APIs',
    author='Jacob Cook',
    author_email='jacob@coderouge.co',
    url='https://git.coderouge.co/coderouge/python-ngrok',
    py_modules=['ngrok'],
    download_url = 'https://git.coderouge.co/coderouge/python-ngrok/repository/archive.tar.gz?ref=0.1',
    license = 'GPLv3'
)
