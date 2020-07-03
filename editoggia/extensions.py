# extensions.py --- 
# 
# Filename: extensions.py
# Author: Louise <louise>
# Created: Sat May  2 06:11:47 2020 (+0200)
# Last-Updated: Fri Jul  3 17:15:34 2020 (+0200)
#           By: Louise <louise>
# 
"""
Create all extension objects. They are then initialized
with the app in the app factory.
"""
from flask_babel import Babel
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

babel = Babel()
lm = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

@babel.localeselector
def get_locale():
    """
    Returns the locale the app should use.
    """
    from flask import request, current_app
    from flask_login import current_user
    
    # if a user is logged in, use the locale from the user settings
    if current_user.is_authenticated:
        return current_user.language
    
    # otherwise try to guess the language from the user accept
    # header the browser transmits.
    return request.accept_languages.best_match(
        current_app.config["ACCEPTED_LANGUAGES"]
    )
