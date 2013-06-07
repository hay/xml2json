import os

from setuptools import setup, find_packages

setup(
    name = "xml2json",
    version = "0.1",
    author = "Hay Kranen",
    author_email = "huskyr@gmail.com",
    description = ("Python script converts XML to JSON or the other way around"),
    license = "LICENSE",
    keywords = "xml json",
    url = "http://github.com/hay/xml2json",
    #packages=find_packages(exclude=['ez_setup']),
    py_modules=['xml2json'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        ],
    install_requires=[
        'simplejson'
        ],
    entry_points="""
            [console_scripts]
            xml2json = xml2json:xml2json
          """,
    )
