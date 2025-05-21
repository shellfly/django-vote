import os
from setuptools import setup, find_packages

import vote


with open("README.md") as f:
    README = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-vote",
    version=".".join(str(i) for i in vote.VERSION),
    packages=find_packages(exclude=("test*",)),
    include_package_data=True,
    description="A simple Django app to conduct vote.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/shellfly/django-vote",
    author="shellfly",
    author_email="shell0fly@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.7",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
)
