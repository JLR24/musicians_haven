from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from ..models import db, Help

help = Blueprint("help", __name__, template_folder="templates", static_folder="static")


@help.route("/")
def Home():
    '''This page displays the site map and links for other help sources'''
    return render_template("help.html", user=current_user, active="Home")


@help.route("/faq")
def FAQ():
    '''This page displays FAQs to the user'''
    return render_template("faq.html", user=current_user, active="FAQ")


@help.route("/contact")
def Contact():
    '''This page allows the user to submit a help form'''
    return render_template("contact.html", user=current_user, active="Contact")


@help.route("/HandleContact", methods=["POST"])
def HandleContact():
    '''This page handles the contact form submission'''
    db.session.add(Help(
        email = request.form.get("email"),
        question = request.form.get("query")
    ))
    db.session.commit()
    flash("You query has been submitted! Please allow 7-10 working days for a response.", category="success")
    return redirect(url_for("help.Home"))