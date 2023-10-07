from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from ..models import db
from .static.admin_utilities import IsAdmin

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin.route("/")
def Home():
    '''This function displays the admin home page'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    return render_template("admin_home.html", user=current_user)