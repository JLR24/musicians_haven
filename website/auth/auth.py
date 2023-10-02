from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required, logout_user
from .static.auth_utilities import IsLoggedIn

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route("/login", methods=["POST", "GET"])
def Login():
    '''This page allows the user to login to their account'''
    if IsLoggedIn():
        return redirect(url_for("mh.Home"))
    return render_template("login.html", user=current_user)


@auth.route("/signup")
def Signip():
    '''This page allows the user to signup to a new account'''
    if IsLoggedIn():
        return redirect(url_for("mh.Home"))
    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def Logout():
    '''This page allows the user to sign out of their account'''
    flash("Logged out!", category="success")
    logout_user()
    return redirect(url_for("auth.Login"))
