# manage.py --- 
# 
# Filename: manage.py
# Author: Louise <louise>
# Created: Mon May  4 01:27:39 2020 (+0200)
# Last-Updated: Mon May  4 01:28:23 2020 (+0200)
#           By: Louise <louise>
# 
from flask_script import Manager
from editoggia import app

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
