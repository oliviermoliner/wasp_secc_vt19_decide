import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    README = f.read()

requires = ["numpy"]

tests_require = ["pytest"]

setup(
    name="decide",
    version="0.0",
    description="decide",
    long_description=README,
    classifiers=["Programming Language :: Python"],
    author="Olivier Moliner",
    author_email="olivier.moliner@gmail.com",
    url="",
    keywords="homework",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={"testing": tests_require},
    install_requires=requires,
)
