# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Tue May  5 02:33:30 2020 (+0200)
# Last-Updated: Tue May  5 02:33:54 2020 (+0200)
#           By: Louise <louise>
# 
from app.extensions import lm

@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))
