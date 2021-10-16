# setup.py ---
#
# Filename: setup.py
# Author: Louise <louise>
# Created: Fri May  8 20:18:07 2020 (+0200)
# Last-Updated: Sun Jul 12 14:01:22 2020 (+0200)
#           By: Louise <louise>
#
from setuptools import setup

setup(
    name="editoggia",
    version="1.0",
    packages=["editoggia"],
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-admin",
        "flask-assets",
        "flask-babelex",
        "flask-login",
        "flask-bcrypt",
        "flask-migrate",
        "flask-sqlalchemy",
        "flask-wtf",
        "libsass",
        "bs4",
        "bleach",
        "arrow",
        "email-validator",
        "faker",
    ],
)
