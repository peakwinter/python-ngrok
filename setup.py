#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='python-ngrok',
    version='0.1',
    description='Python bindings for ngrok local and Link APIs',
    author='Jacob Cook',
    author_email='jacob@coderouge.co',
    url='https://git.coderouge.co/coderouge/python-ngrok',
    packages=find_packages(),
    download_url = 'https://git.coderouge.co/coderouge/python-ngrok/repository/archive.tar.gz?ref=0.1',
    license = 'GPLv3'
)
