#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

__VERSION__ = '0.0.10'

assert sys.version_info[0] == 3, "Graphene-PriceFeed requires Python > 3"

setup(
    name='graphene-pricefeed',
    version=__VERSION__,
    description='Command line tool to assist with price feed generation',
    long_description=open('README.md').read(),
    download_url='https://github.com/xeroc/bitshares-pricefeed/tarball/' + __VERSION__,
    author='Fabian Schuh',
    author_email='Fabian@chainsquad.com',
    maintainer='Fabian Schuh',
    maintainer_email='Fabian@chainsquad.com',
    url='https://github.com/graphene-blockchain/graphene-pricefeed',
    keywords=['graphene', 'price', 'feed', 'cli'],
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    entry_points={
        'console_scripts': [
            'graphene-pricefeed = bitshares_pricefeed.cli:main'
        ],
    },
    install_requires=[
        "requests==2.22.0",  # Required by graphenlib
        "bitshares",
        "uptick",
        "prettytable",
        "click",
        "colorama",
        "tqdm",
        "pyyaml",
        "quandl"
    ],
    extras_require={
        'history_db_postgresql': ["SQLAlchemy", "py-postgresql"]
    },
    dependency_links=[
        'git+https://github.com/graphene-blockchain/python-bitshares#egg=bitshares',
        'git+https://github.com/graphene-blockchain/uptick#egg=uptick'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
