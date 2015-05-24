import sys
from setuptools import setup


setup(
    name='mailthon',
    version='0.0.0',
    description='Elegant email library',
    long_description=open('README.rst').read(),
    author='Eeo Jun',
    author_email='packwolf58@gmail.com',
    url='https://github.com/eugene-eeo/mailthon/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    include_package_data=True,
    package_data={'mailthon': ['LICENSE', 'README.rst']},
    packages=['mailthon'],
    tests_require=['pytest'],
)
