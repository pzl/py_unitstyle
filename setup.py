from setuptools import setup, find_packages

from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


setup(
      name='unitstyle',
      version='1.0.0',
      description='Adds various style choices to unittest output',
      url='https://github.com/pzl/py_unitstyle',
      author='Dan Panzarella',
      author_email='dan@panzarel.la',
      license='MIT',
      classifiers = [
      	'Development Status :: 4 - Beta',
      	'Environment :: Console',
      	'Intended Audience :: Developers',
      	'License :: OSI Approved :: MIT License',
      	'Programming Language :: Python :: 2',
      	'Programming Language :: Python :: 2.6',
      	'Programming Language :: Python :: 2.7',
      	'Programming Language :: Python :: 3',
      	'Programming Language :: Python :: 3.3',
      	'Programming Language :: Python :: 3.4',
      	'Programming Language :: Python :: 3.5',
      	'Topic :: Software Development :: Testing'
      ],
      keywords='test testing unittest unitstyle console development',
      packages=['unitstyle'],


)