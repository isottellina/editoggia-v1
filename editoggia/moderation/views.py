# views.py ---
#
# Filename: views.py
# Author: Louise <louise>
# Created: Sat Jul 11 21:13:04 2020 (+0200)
# Last-Updated: Sat Jul 11 23:01:52 2020 (+0200)
#           By: Louise <louise>
#
from flask import render_template, abort, url_for, redirect
from flask_login import current_user, login_required

from editoggia.database import db
from editoggia.models import Fandom, FandomCategory, Tag

from editoggia.moderation.forms import FandomsForm, TagsForm
from editoggia.moderation import moderation

@moderation.before_request
def check_permission():
    """
    This is executed before every request to check if
    the user has moderation permission. None of the views
    in this blueprint can be accessed without permission.
    """
    if not current_user.has_permission("mod.ACCESS_TAG_INTERFACE"):
        abort(403)

@moderation.route('/')
def index():
    return render_template('moderation/index.jinja2')

@moderation.route('/fandoms', methods=["GET", "POST"])
def fandoms():
    """
    The interface to edit fandoms who are waiting for moderations.
    """
    # Get all fandoms who need moderation
    waiting_fandoms = db.session.query(Fandom) \
                                .filter(Fandom.waiting_mod == True) \
                                .all()

    # Create the form and validate it
    form = FandomsForm()
    if form.validate_on_submit():
        # Now we just have to set the data on all fandoms
        for fandom_form in form.fandoms.entries:
            fandom = Fandom.get_by_id_or_404(fandom_form.data['id'])
            category = FandomCategory.get_by_name_or_404(fandom_form.data['category'])

            fandom.update(
                name=fandom_form.data['name'],
                category=category,
                waiting_mod=False
            )
        return redirect(url_for('moderation.index'))

    # If we only have GET, fill the forms.

    for fandom in waiting_fandoms:
        form.fandoms.append_entry(fandom)

    return render_template("moderation/fandoms.jinja2", form=form)

@moderation.route('/tags', methods=["GET", "POST"])
def tags():
    """
    The interface to edit tags who are waiting for moderations.
    """
    # Get all fandoms who need moderation
    waiting_tags = db.session.query(Tag) \
                                .filter(Tag.waiting_mod == True) \
                                .all()

    # Create the form and validate it
    form = TagsForm()
    if form.validate_on_submit():
        # Now we just have to set the data on all tags
        for tag_form in form.tags.entries:
            tag = Tag.get_by_id_or_404(tag_form.data['id'])

            tag.update(
                name=tag_form.data['name'],
                waiting_mod=False
            )
        return redirect(url_for('moderation.index'))

    # If we only have GET, fill the forms.
    for tag in waiting_tags:
        form.tags.append_entry(tag)

    return render_template("moderation/tags.jinja2", form=form)
