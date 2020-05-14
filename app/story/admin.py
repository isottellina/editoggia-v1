# admin.py --- 
# 
# Filename: admin.py
# Author: Louise <louise>
# Created: Thu May 14 20:03:35 2020 (+0200)
# Last-Updated: Thu May 14 20:06:07 2020 (+0200)
#           By: Louise <louise>
# 
from app.admin import EditoggiaModelView, admin
from app.database import db
from app.story.models import Fandom, Fiction, Chapter, Tag

admin.add_view(EditoggiaModelView(Fandom,
                                  db.session,
                                  category="Stories",
                                  endpoint='admin_fandom')
)

admin.add_view(EditoggiaModelView(Fiction,
                                  db.session,
                                  category="Stories",
                                  endpoint='admin_story')
)

admin.add_view(EditoggiaModelView(Chapter,
                                  db.session,
                                  category="Stories",
                                  endpoint='admin_chapter')
)

admin.add_view(EditoggiaModelView(Tag,
                                  db.session,
                                  category="Stories",
                                  endpoint='admin_tag')
)
