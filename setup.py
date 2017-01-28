
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyMech',
    version='0.0.1a',
    description='Roloff / Matek brought to Python',
    long_description=long_description,
    url='https://github.com/peer23peer/pyMech',
    author='Jelle Spijker',
    author_email='spijker.jelle@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Mechanical engineers',
        'Topic :: Engineering :: designer',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='mechanical engineering',
    packages=find_packages(),
    install_requires=['numpy', 'pint'],

)
