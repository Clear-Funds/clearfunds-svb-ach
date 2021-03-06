import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='clearfunds_svb_ach',
    version='0.0.1',
    author='Synares',
    author_email='saad@synares.com',
    description='SVB-ACH for clearfunds',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Synares/clearfunds-svb-ach.git',
    license='MIT',
    packages=['clearfunds_svb_ach'],
    install_requires=['certifi',
                      'chardet',
                      'idna',
                      'urllib3',
                      'requests'],
)