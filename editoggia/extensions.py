# extensions.py ---
#
# Filename: extensions.py
# Author: Louise <louise>
# Created: Sat May  2 06:11:47 2020 (+0200)
# Last-Updated: Thu Jul  9 17:54:19 2020 (+0200)
#           By: Louise <louise>
#
"""
Create all extension objects. They are then initialized
with the app in the app factory.
"""
from flask_babelex import Babel
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

babel = Babel()
lm = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()


#
# This is where the locale selector function should be.
# If it's not here, it's because apparently for now it
# triggers an exception in Flask-Admin. Since it's not
# needed, since the only locale the website is translated
# in is English, I decided to remove it. I will however
# keep all other things, like the language selector on
# the profile, to be able to re-add the locale selector
# as easily as possible once the issue is resolved.
#
@babel.localeselector
def get_locale():
    """
    Returns the locale the app should use.
    """
    from flask import current_app, request
    from flask_login import current_user

    # If there is no current_user, even anonymous, that means
    # we are outside of request context
    if not current_user:
        return current_app.config["BABEL_DEFAULT_LOCALE"]

    # if a user is logged in, use the locale from the user settings
    if current_user.is_authenticated and current_user.language:
        return current_user.language

    # otherwise try to guess the language from the user accept
    # header the browser transmits.
    return request.accept_languages.best_match(current_app.config["ACCEPTED_LANGUAGES"])
