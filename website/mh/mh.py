from flask import Blueprint, render_template, flash, request
from flask_login import current_user
from .static.paginator import Paginator
from ..models import db

mh = Blueprint("mh", __name__, template_folder="templates", static_folder="static")

@mh.route("/")
def Home():
    if current_user.is_authenticated:
        # In case admin status is ever reset, set rank to admin.
        if current_user.username == "JLR24" and current_user.status != "Admin":
            current_user.status = "Admin"
            flash(" >> Promoted JLR24 to admin", category="info")
            db.session.commit()
        feed = current_user.getFeed()
        if not feed:
            feed = []
            # feed.append(UserPost(caption="Testing Posts", user=1, date=datetime.datetime.now()))
        p = Paginator(feed, 12)
        page = request.args.get("page")
        if not page:
            page = 1
        return render_template("home_logged_in.html", user=current_user, p=p, page=page)
    return render_template("home_logged_out.html", user=current_user)
    

@mh.route("/about")
def About():
    '''This page displays the "about the site" information to the user'''
    return render_template("about.html")


@mh.route("/thanks")
def Thanks():
    '''This page displays the "special thanks" information to the user'''
    return render_template("thanks.html")