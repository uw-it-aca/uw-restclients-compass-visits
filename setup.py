import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/uw-restclients-compass-visits>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = "uw_compass_visits/VERSION"
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/uw-restclients-compass-visits"
setup(
    name="UW-RestClients-compass-visits",
    version=VERSION,
    packages=["uw_compass_visits"],
    author="UW-IT Student & Educational Technology Services",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=["UW-RestClients-Core"],
    license="Apache License, Version 2.0",
    description=(
        "A library for connecting to Compass visits service at the "
        "University of Washington"
    ),
    long_description=README,
    url=url,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
