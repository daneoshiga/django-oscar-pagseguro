import re
from setuptools import setup, find_packages


version = None
with open('oscar_pagseguro/__init__.py', 'r') as fd:
        version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                            fd.read(), re.MULTILINE).group(1)

setup(
    name='django-oscar-pagseguro',
    version=version,
    url='https://github.com/daneoshiga/django-oscar-pagseguro',
    download_url='https://github.com/daneoshiga/django-oscar-pagseguro/tarball/0.0.2',
    author="Danilo Shiga",
    author_email="daniloshiga@gmail.com",
    description="Pagseguro integration paypal",
    long_description=open('README.rst').read(),
    keywords="Payment, Pagseguro, Oscar",
    license=open('LICENSE').read(),
    platforms=['linux'],
    packages=find_packages(exclude=['sandbox*', 'tests*']),
    include_package_data=True,
    install_requires=[
        "django-oscar>=0.6",
        'django-pagseguro2>=1.0',
    ],
    extras_require={
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
        'Topic :: Other/Nonlisted Topic'],
)
