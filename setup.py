import os
from setuptools import setup, find_packages

import vote


with open('README.md') as f:
    README = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-vote',
    version='.'.join(str(i) for i in vote.VERSION),
    packages=find_packages(exclude=('test*',)),
    include_package_data=True,
    license='BSD License',
    description='A simple Django app to conduct vote.',
    long_description=README,
    url='https://github.com/Beeblio/django-vote',
    author='shellfly',
    author_email='shell0fly@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
)
