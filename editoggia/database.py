# database.py ---
#
# Filename: database.py
# Author: Louise <louise>
# Created: Sat May  9 00:22:37 2020 (+0200)
# Last-Updated: Tue May 19 18:32:05 2020 (+0200)
#           By: Louise <louise>
#
"""
Creates database objects and Mixins
"""
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
