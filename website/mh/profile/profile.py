from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from ...models import db

profile = Blueprint("profile", __name__, template_folder="templates", static_folder="static")

@profile.route("/")
def Current():
    '''Displays the profile of the current user'''
    return render_template("current_profile.html", user=current_user, active="Home")