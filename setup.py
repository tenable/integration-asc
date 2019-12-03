from setuptools import setup, find_packages
import os

long_description = '''
Tenable.io -> Microsoft Azure Security Center Bridge
For usage documentation, please refer to the github repository at
https://github.com/tenable/integrations-microsoft-asc
'''

setup(
    name='tenable-microsoft-asc',
    version='1.0.1',
    description='',
    author='Tenable, Inc.',
    long_description=long_description,
    author_email='smcgrath@tenable.com',
    url='https://github.com/tenable/integrations-microsoft-asc',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Topic :: System :: Networking',
        'Topic :: Other/Nonlisted Topic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='tenable tenable_io microsoft securitycenter',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pytenable>=0.3.28',
        'restfly>=1.1.0',
        'arrow>=0.14.0',
        'Click>=7.0'
    ],
    entry_points={
        'console_scripts': [
            'tenable-asc=tenable_asc.cli:cli',
        ],
    },
)