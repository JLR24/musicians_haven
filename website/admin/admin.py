from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from ..models import db, User, Help, Missing
from .static.admin_utilities import IsAdmin, GetAdmins, GetEditors, GetMax, GetBanned, EmailHelpResponse, EmailMissingResponse

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin.route("/")
@login_required
def Home():
    '''This function displays the admin home page'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    admins = GetAdmins()
    editors = GetEditors()
    return render_template("admin_home.html", user=current_user, active="Dashboard", m=GetMax([admins, editors]), admins=admins, editors=editors)


@admin.route("/bans")
@login_required
def Bans():
    '''This page displays the admin ban page'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    return render_template("admin_ban.html", user=current_user, active="Bans", banned=GetBanned())


@admin.route("/help")
@login_required
def HelpResponse():
    '''This page displays the admin help response page'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    response = request.args.get("r")
    return render_template("admin_help.html", user=current_user, active="Help", queries=Help.query.all(), response=response)


@admin.route("/missing")
@login_required
def MissingReports():
    '''This page displays the admin missing reports response page'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    response = request.args.get("r")
    return render_template("admin_missing.html", user=current_user, active="Missing", missing=Missing.query.all(), response=response)


# @admin.route("/logs")
# @login_required
# def Logs():
#     '''This page allows the admins to view and filter logs'''
#     if not IsAdmin():
#         return redirect(url_for("home.Home"))
#     return render_template("admin_logs.html", user=current_user, active="Logs")


@admin.route("/HandleAdminPromote", methods=["POST"])
@login_required
def HandleAdminPromote():
    '''This page handles the promote new admin form submission'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    user = User.query.filter_by(username=request.form.get("username")).first()
    if not user:
        flash("Couldn't find a user with that name...", category="error")
        return redirect(url_for("admin.Home"))
    if user in GetAdmins():
        return redirect(url_for("admin.Home"))
    user.status = "Admin"
    db.session.commit()
    flash("User has been promoted!", category="success")
    return redirect(url_for("admin.Home"))


@admin.route("/HandleEditorPromote", methods=["POST"])
@login_required
def HandleEditorPromote():
    '''This page handles the promote new editor form submission'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    user = User.query.filter_by(username=request.form.get("username")).first()
    if not user:
        flash("Couldn't find a user with that name...", category="error")
        return redirect(url_for("admin.Home"))
    if user in GetEditors():
        return redirect(url_for("admin.Home"))
    if user in GetAdmins():
        flash("User is already an admin, cannot demote.", category="error")
        return redirect(url_for("admin.Home"))
    user.status = "Editor"
    db.session.commit()
    flash("User has been promoted!", category="success")
    return redirect(url_for("admin.Home"))


@admin.route("/HandleAdminDemote", methods=["POST"])
@login_required
def HandleAdminDemote():
    '''This page handles the demote admin form submission'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    user = User.query.filter_by(username=request.form.get("username"), status="Admin").first()
    if not user:
        flash("Couldn't find an admin with that name...", category="error")
        return redirect(url_for("admin.Home"))
    if user.username == "JLR24":
        flash("You can't demote JLR24...", category="error")
        return redirect(url_for("admin.Home"))
    user.status = "User"
    db.session.commit()
    flash("User has been demoted!", category="success")
    return redirect(url_for("admin.Home"))


@admin.route("/HandleEditorDemote", methods=["POST"])
@login_required
def HandleEditorDemote():
    '''This page handles the demote editor form submission'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    user = User.query.filter_by(username=request.form.get("username"), status="Editor").first()
    if not user:
        flash("Couldn't find an editor with that name...", category="error")
        return redirect(url_for("admin.Home"))
    user.status = "User"
    db.session.commit()
    flash("User has been promoted!", category="success")
    return redirect(url_for("admin.Home"))


@admin.route("/HandleBan", methods=["POST"])
@login_required
def HandleBan():
    '''This page handles the banning of a user'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    user = User.query.filter_by(username=request.form.get("username")).first()
    if not user or user.username == "JLR24":
        flash("Error: unable to ban.", category="error")
        return redirect(url_for("admin.Bans"))
    user.status = "Banned: " + request.form.get("reason")
    db.session.commit()
    flash("User successfully banned!", category="success")
    return redirect(url_for("admin.Bans"))


@admin.route("/HandlePardon", methods=["POST"])
@login_required
def HandlePardon():
    '''This page handles the pardoning of a user'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    user = User.query.filter_by(username=request.form.get("username")).first()
    if not user or not user in GetBanned():
        flash("Error: Could not pardon this user", category="error")
        return redirect(url_for("admin.Bans"))
    user.status = "User"
    db.session.commit()
    flash("User successfully pardoned!", category="success")
    return redirect(url_for("admin.Bans"))


@admin.route("/HandleHelpResponse", methods=["POST"])
@login_required
def HandleHelpResponse():
    '''This page handles the response to a help query'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    help = Help.query.filter_by(id=request.form.get("id")).first()
    if not help:
        flash("Invalid details!", category="error")
        return redirect(url_for("admin.Home"))
    response = request.form.get("response")
    if not EmailHelpResponse(help, response):
        flash("Error sending email, please try again")
        return redirect(url_for("admin.HelpResponse", r=response))
    # Delete Help object from db
    db.session.delete(help)
    db.session.commit()
    return redirect(url_for("admin.HelpResponse"))


@admin.route("/HandleMissing", methods=["POST"])
@login_required
def HandleMissing():
    '''This page handles the response to missing report'''
    if not IsAdmin():
        return redirect(url_for("home.Home"))
    missing = Missing.query.filter_by(id=request.form.get("id")).first()
    if not missing:
        flash("Invalid details!", category="error")
        return redirect(url_for("admin.Home"))
    response = request.form.get("response")
    if missing.email and response and len(response) > 0:
        if not EmailMissingResponse(missing, response):
            flash("Error sending email, please try again")
            return redirect(url_for("admin.MissingReports", r=response))
    # Delete Help object from db
    db.session.delete(missing)
    db.session.commit()
    return redirect(url_for("admin.MissingReports"))