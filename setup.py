import setuptools
from setuptools import find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='clearfunds_svb_ach',
    version='0.0.2',
    author='Synares',
    author_email='saad@synares.com',
    description='SVB-ACH for clearfunds',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Clear-Funds/clearfunds-svb-ach',
    license='MIT',
    packages=find_packages(),
    install_requires=['certifi',
                      'chardet',
                      'idna',
                      'urllib3',
                      'requests',
                      'jwcrypto'],
)
