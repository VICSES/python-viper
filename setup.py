from setuptools import setup, find_packages
import os

rootdir = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(rootdir, 'README.md')).read()

setup (
    name='Viper',
    version='1.0.0',

    description='Send VICSES EAS pages via Viper',
    long_description=long_description,

    url='https://github.com/VICSES/Python-Viper',

    author='David Tulloh',
    author_email='vicsesdev-david@tulloh.id.au',

    license='AGPL-3+',

    keywords='VICSES EAS paging',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Topic :: Communications',
        'Programming Language :: Python :: 3',
    ],

    py_modules=["viper"],

    install_requires=['requests'],

    extras_require={
            'dev': ['check-manifest'],
            'test': ['coverage'],
    },

    package_data={},
)
