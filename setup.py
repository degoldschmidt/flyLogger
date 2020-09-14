import os, sys
from setuptools import setup
from setuptools import find_packages
import distutils.util

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if sys.version_info[0] == 3:
    LONG_DESCRIPTION = open('README.rst', encoding='utf-8').read()
else:
    LONG_DESCRIPTION = open('README.rst').read()

setup(
    name="flylogger",
    version="1.0",
    author="Dennis Goldschmidt",
    author_email="dennis.goldschmidt@neuro.fchampalimaud.org",
    description=("Logging API for fly experiments: from stocks to experimental metadata fully automated."),
    license="GPLv3",
    keywords=['tracking', 'data analysis', 'fly'],
    url="https://pypi.python.org/pypi/pytrack",
    packages=['flylogger'],
    python_requires='>=3.6',
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
    ],
    platforms=['Windows10Pro', 'MacOSX-HighSierra'],
    setup_requires=['numpy', 'pyyaml', 'pandas', 'scipy', 'matplotlib', 'seaborn', 'google-api-python-client', 'httplib2', 'gspread', 'oauth2client', 'PyOpenSSL', 'pygsheets', 'pandastable'],
    entry_points={
        'gui_scripts': [
            'flylogger = flylogger.main:main',
        ],
    },
)
