import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    README = f.read()

INSTALL_REQUIRES = ["numpy"]

EXTRAS_REQUIRE = {
    "testing": ["pytest"],
    "lint": ["black==18.9b0", "pre-commit==1.14.3"],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"]


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
    extras_require=EXTRAS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
)
