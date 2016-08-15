from distutils.core import setup

DISTNAME='flowspace'
FULLVERSION='0.1'

setup(
    name=DISTNAME,
    version=FULLVERSION,
    packages=['flowspace'],
    entry_points={
        'console_scripts':
            [
            ]
    },
    install_requires = [
    ]
)
