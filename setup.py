from os import path
from setuptools import setup, find_packages

# Project
NAME = 'GeoLocationExtender'
VERSION = '0.1.0'

# Authors and maintainers
AUTHORS = 'Aron Horvath (@arcsi1989)'
MAINTAINER = ''
MAINTAINER_EMAIL = 'arcsi1989@gmail.com'

# License
LICENSE = 'MIT'

# Project URLs
REPOSITORY = 'TODO add repository'  # TODO
HOMEPAGE = 'TODO Add home page - could be the repository'  # TODO
PROJECT_URLS = {
    'Bug Tracker': f'{REPOSITORY}/issues',
    'Documentation': HOMEPAGE,
    'Source Code': REPOSITORY,
}
DOWNLOAD_URL = ''

# Classifiers
CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Environment :: Console",
    "Operating System :: OS Independent",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License"
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.7",
    "Framework :: Pytest",
    "Framework :: Flake8",
]

# Long description
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    INSTALL_REQUIREMENTS = f.read().splitlines()

# Package definition
setup(name=NAME,
      # version=VERSION,
      description='TODO Description of the project',  # TODO
      # url=HOMEPAGE,
      packages=find_packages(where='.', include=['src']),
      author=AUTHORS,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      license=LICENSE,
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      # download_url=DOWNLOAD_URL,
      # project_urls=PROJECT_URLS,
      python_requires='>3.7.0',
      install_requires=INSTALL_REQUIREMENTS,
      entry_points={
          'console_scripts': [
              'geo_loc_extend = src.main:address_enriching_program',
          ]
      },
      include_package_data=True,
      zip_safe=False,
      )
