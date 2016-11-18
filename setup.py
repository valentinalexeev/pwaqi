#!/usr/bin/env python

from distutils.core import setup

setup(name='pwaqi',
	version='1.2',
	description='Python wrapper for World Air Quality Index data',
	author='Valentin Alexeev',
	author_email='valentin.alekseev@gmail.com',
	url='https://github.com/valentinalexeev/pwaqi',
	packages=['pwaqi'],
	install_requires=['requests']
)