
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')


setup(
    long_description=readme,
    name='rasam',
    version='0.4.2',
    description='Rasa Improved',
    python_requires='<3.9,>=3.6.2',
    project_urls={"repository": "https://github.com/roniemartinez/rasam"},
    author='Ronie Martinez',
    author_email='ronmarti18@gmail.com',
    license='MIT',
    keywords='URL extractor for Rasa Regex entity extractor for Rasa Placeholder importer for Rasa',
    classifiers=['Development Status :: 3 - Alpha', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: CPython'],
    packages=['rasam'],
    package_dir={"": "."},
    package_data={},
    install_requires=['faker<10.0.0,>=8.1.4', 'rasa==2.*,>=2.8.12', 'urlextract==1.*,>=1.2.0'],
    extras_require={"dev": ["autoflake==1.*,>=1.3.1", "black==21.7b0", "codecov==2.*,>=2.1.12", "dephell==0.*,>=0.8.2", "flake8==4.*,>=4.0.1", "isort==5.*,>=5.10.1", "mistune<2.0.0", "mypy==0.*,>=0.910.0", "pyproject-flake8==0.*,>=0.0.1.a2", "pytest==6.*,>=6.2.5", "pytest-asyncio==0.*,>=0.16.0", "pytest-cov==3.*,>=3.0.0", "tomlkit==0.7.0"]},
)
