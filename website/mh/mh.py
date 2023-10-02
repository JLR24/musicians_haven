from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required

mh = Blueprint("mh", __name__, template_folder="templates", static_folder="static")

@mh.route("/")
def Home():
    return "<p>WIP</p> <a href=/auth/login>Login</a>"
    