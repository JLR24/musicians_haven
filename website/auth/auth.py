from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import current_user, login_required, logout_user, login_user
from .static.auth_utilities import IsLoggedIn, GetUser, GetRedirectAddress, CheckUser, SendSignupToken, GenerateToken, CheckToken, AddUser
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route("/")
@auth.route("/login")
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


@auth.route("/validate/<string:token>")
def Validate(token):
    '''Checks that the user's token is valid'''
    if IsLoggedIn():
        return redirect(url_for("mh.Home"))
    try:
        CheckToken(token)
    except:
        flash("That validation link is either invalid, or has expired. Please request another.", category="error")
        session.clear()
        return redirect(url_for("auth.Signup"))
    user = AddUser()
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


# NOTE: To add: /forgot_password and /reset/<token>


@auth.route("/HandleLogin", methods=["POST"])
def HandleLogin():
    '''This page handles the login form submission'''
    if IsLoggedIn():
        return redirect(url_for("mh.Home"))
    key = request.form.get("key")
    password = request.form.get("pw")
    user = GetUser(key)
    if user and check_password_hash(user.password, password):
        login_user(user, remember=True)
        flash(f"Login successful. Welcome back, {user.username}!", category="success")
        return redirect(GetRedirectAddress())
    flash("Invalid login details. Please try again...", category="error")
    return redirect(url_for("auth.Login"))


@auth.route("/HandleSignup", methods=["POST"])
def HandleSignup():
    '''This page handles the signup form submission'''
    if IsLoggedIn():
        return redirect(url_for("mh.Home"))
    session["username"] = request.form.get("un")
    session["email"] = request.form.get("email")
    session["pw"] = request.form.get("pw1")

    if not CheckUser(session["username"], session["email"]):
        session.clear()
        flash("These details have already been used, please try again.", category="error")
        return redirect(url_for("auth.Signup"))
    SendSignupToken(GenerateToken())
    return '''<div style="padding:10px; border: 1px solid black; margin: 15px">
        <h1>Your email has been sent a verification link.</h1><br>
        <p>Please click it to activate your account.</p>
    </div>'''