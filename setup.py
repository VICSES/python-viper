from setuptools import setup, find_packages
import os

long_description= (
  'The Victoria State Emergency Service uses an online tool called Viper '
  'to send Emergency Alerting System (EAS) pages. This online form based '
  'system is difficult to extend and use in other tools.\n\n'
  'This module hides the nasty work of interacting with Viper presenting '
  'a simple interface for scripts to use.'
)

setup (
    name='vicses.viper',
    version='1.0.0',

    description='Send VICSES EAS pages via Viper',
    long_description=long_description,

    url='https://github.com/VICSES/Python-Viper',

    author='David Tulloh',
    author_email='vicsesdev-david@tulloh.id.au',

    license='AGPL-3+',

    keywords='Viper VICSES EAS paging',

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
