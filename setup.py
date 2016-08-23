import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests', '--cov=mailthon']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='mailthon',
    version='0.2.0',
    description='Elegant email library',
    long_description=open('README.rst', 'rb').read().decode('utf8'),
    author='Eeo Jun',
    author_email='141bytes@gmail.com',
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
    tests_require=[
        'mock',
        'pytest',
        'pytest-localserver',
        'pytest-cov',
        ],
    cmdclass={'test': PyTest},
    platforms='any',
    zip_safe=False,
)
