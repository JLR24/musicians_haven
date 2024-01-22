from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import current_user, login_required, logout_user, login_user
from .static.auth_utilities import is_logged_in, get_user, get_redirect_address, check_user, send_signup_token, generate_token, check_token, add_user
from werkzeug.security import check_password_hash
from ..models import User

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route("/")
@auth.route("/login")
def Login():
    '''This page allows the user to login to their account'''
    if is_logged_in():
        return redirect(url_for("mh.Home"))
    return render_template("login.html", user=current_user)


@auth.route("/signup")
def Signip():
    '''This page allows the user to signup to a new account'''
    if is_logged_in():
        return redirect(url_for("mh.Home"))
    return render_template("signup.html", user=current_user)


@auth.route("/validate/<string:token>")
def Validate(token):
    '''Checks that the user's token is valid'''
    if is_logged_in():
        return redirect(url_for("mh.Home"))
    try:
        check_token(token)
    except:
        flash("That validation link is either invalid, or has expired. Please request another.", category="error")
        session.clear()
        return redirect(url_for("auth.Signup"))
    user = add_user()
    session.clear()
    login_user(user, remember=True)
    flash(f"Account created successfully. Welcome, {user.username}! Make sure to update your profile and settings.", category="success")
    return redirect(url_for("mh.Home"))


@auth.route("/logout")
@login_required
def Logout():
    '''This page allows the user to sign out of their account'''
    flash("Logged out!", category="success")
    logout_user()
    return redirect(url_for("auth.Login"))


@auth.route("/banned")
def Banned():
    '''This page explains why the user has been banned'''
    user = User.query.filter_by(id=request.args.get("id")).first()
    if not user or not user.status[0] == "B":
        return redirect(url_for("auth.Login"))
    try:
        reason = user.getBanReason()
        return render_template("banned.html", user=current_user, reason=reason)
    except:
        return redirect(url_for("auth.Login"))


# NOTE: To add: /forgot_password and /reset/<token>


@auth.route("/HandleLogin", methods=["POST"])
def HandleLogin():
    '''This page handles the login form submission'''
    if is_logged_in():
        return redirect(url_for("mh.Home"))
    key = request.form.get("key")
    password = request.form.get("pw")
    user = get_user(key)
    if user and check_password_hash(user.password, password):
        if user.status[0] == "B":
            return redirect(url_for("auth.Banned", id=user.id))
        login_user(user, remember=True)
        flash(f"Login successful. Welcome back, {user.username}!", category="success")
        return redirect(get_redirect_address())
    flash("Invalid login details. Please try again...", category="error")
    return redirect(url_for("auth.Login"))


@auth.route("/HandleSignup", methods=["POST"])
def HandleSignup():
    '''This page handles the signup form submission'''
    if is_logged_in():
        return redirect(url_for("mh.Home"))
    session["username"] = request.form.get("un")
    session["email"] = request.form.get("email")
    session["pw"] = request.form.get("pw1")

    if not check_user(session["username"], session["email"]):
        session.clear()
        flash("These details have already been used, please try again.", category="error")
        return redirect(url_for("auth.Signup"))
    send_signup_token(generate_token())
    return '''<div style="padding:10px; border: 1px solid black; margin: 15px">
        <h1>Your email has been sent a verification link.</h1><br>
        <p>Please click it to activate your account.</p>
    </div>'''