# admin.py --- 
# 
# Filename: admin.py
# Author: Louise <louise>
# Created: Thu May 14 20:03:35 2020 (+0200)
# Last-Updated: Sat May 30 15:18:23 2020 (+0200)
#           By: Louise <louise>
# 
from editoggia.admin import EditoggiaModelView, admin
from editoggia.database import db
from editoggia.models import Fandom, Story, Chapter, Tag

admin.add_view(EditoggiaModelView(Fandom,
                                  db.session,
                                  category="Stories",
                                  endpoint='admin_fandom')
)

admin.add_view(EditoggiaModelView(Story,
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
