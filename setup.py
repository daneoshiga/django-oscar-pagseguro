#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-oscar-pagseguro',
    version='0.0.2',
    url='',
    author="Danilo Shiga",
    author_email="daniloshiga@gmail.com",
    description=(
        "Pagseguro integration paypal"),
    long_description=open('README.rst').read(),
    keywords="Payment, Pagseguro, Oscar",
    license=open('LICENSE').read(),
    platforms=['linux'],
    packages=find_packages(exclude=['sandbox*', 'tests*']),
    include_package_data=True,
    install_requires=[
    ],
    extras_require={
        'oscar': ["django-oscar>=0.6"]
    },
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Other/Nonlisted Topic'],
)
