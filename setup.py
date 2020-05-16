# setup.py --- 
# 
# Filename: setup.py
# Author: Louise <louise>
# Created: Fri May  8 20:18:07 2020 (+0200)
# Last-Updated: Fri May  8 20:23:15 2020 (+0200)
#           By: Louise <louise>
# 
from setuptools import setup

setup(
    name='editoggia',
    packages=['editoggia'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-admin',
        'flask-assets',
        'flask-babel',
        'flask-login',
        'flask-migrate',
        'flask-sqlalchemy'
    ],
)
