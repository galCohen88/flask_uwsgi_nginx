import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='pm_office',
      version='1.0',
      description='pm_office',
      author='nevix',
      author_email='gal.nevis@gmail.com',
      packages=['client', 'server'],
      install_requires=['flask==0.11.1', 'pyyaml==3.12', 'requests==2.2.1']
      )
