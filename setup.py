#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import imp

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Avoiding import so we don't execute ambry.__init__.py, which has imports
# that aren't installed until after installation.
meta = imp.load_source('_meta', 'geoid/_meta.py')

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

packages = [
    'geoid'
]

scripts=[ ]

package_data = {"": ['*.html', '*.css', '*.rst']}



classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='geoid',
    version=meta.__version__,
    description='Classes for working with US Census geoids',
    long_description=readme,
    packages=packages,
    package_data=package_data,
    scripts=scripts,
    install_requires=['six'],
    tests_require=['nose'],
    test_suite='nose.collector',
    author=meta.__author__,
    author_email='eric@civicknowledge',
    url='https://github.com/CivicKnowledge/geoid',
    license='LICENSE',
    classifiers=classifiers,
)