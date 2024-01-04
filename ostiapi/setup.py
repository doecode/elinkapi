from setuptools import setup, find_packages

setup(
    name='ostiapi',
    packages=find_packages(),
    version='0.1.11',
    description="A Python module to interface with OSTI's E-Link 2.0's API",
    url='https://github.com/UNKNOWN',
    author='Jacob Samar',
    author_email='elink20beta@osti.gov',
    # license='BSD 3-Clause',
    # install_requires=['requests'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
