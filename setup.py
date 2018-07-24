from distutils.core import setup
import fastentrypoints

DISTNAME='flowspace'
FULLVERSION='0.1'

setup(
    name=DISTNAME,
    version=FULLVERSION,
    packages=['flowspace'],
    entry_points={
        'console_scripts':
            [
                'flowspace=flowspace.cli:cli',
            ]
    },
    install_requires = [
        'click',
        'i3-py',
    ]
)
