"""
To install AttrDict:

    python setup.py install
"""
from setuptools import setup

DESCRIPTION = "A dict with attribute-style access"

try:
    LONG_DESCRIPTION = open("README.rst").read()
except:
    LONG_DESCRIPTION = DESCRIPTION


setup(
    name="dotdict",
    version="1.0.0",
    author="Kiselev Aleksandr",
    author_email="kisel.nf97@gmail.com",
    packages=("dotdict",),
    url="https://github.com/kiselas/DotDict",
    license="MIT License",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ),
    tests_require=(
        "pytest",
        "coverage",
    ),
    zip_safe=True,
)
