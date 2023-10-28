from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify
from flask_login import current_user, login_required
from ...models import db, UserInstrument
from .static.file_reader import GetInstruments, GetCities, GetCountries
import datetime

profile = Blueprint("profile", __name__, template_folder="templates", static_folder="static")

@profile.route("/")
@login_required
def Current():
    '''Displays the profile of the current user'''
    return render_template("current_profile.html", user=current_user, active="Home")


@profile.route("/about")
@login_required
def About():
    '''Displays the possible profile settings to the user'''
    user_instruments = [i.serialise for i in current_user.GetInstruments()]
    return render_template("profile_settings.html", 
        user=current_user, active="Profile", 
        year=datetime.datetime.now().year, 
        instruments=GetInstruments(), 
        user_instruments=user_instruments,
        cities=GetCities(), 
        countries=GetCountries()
    )


@profile.route("/HandleNewInstrument", methods=["POST"])
@login_required
def HandleNewInstrument():
    '''Handles the form submission when the user adds a new instrument'''
    db.session.add(UserInstrument(
        user = current_user.id,
        instrument = request.form.get("instruments"),
        details = request.form.get("details"),
        year = request.form.get("year"),
        level = request.form.get("level")
    ))
    db.session.commit()
    flash("Instrument profile added!", category="success")
    return redirect(url_for("profile.About"))


@profile.route("/HandleUpdateInstrument", methods=["POST"])
@login_required
def HandleUpdateInstrument():
    '''Handles the form submission when the user updates an existing instrument'''
    inst = UserInstrument.query.filter_by(user=current_user.id, instrument=request.form.get("instruments")).first()
    if not inst:
        print(request.form.get("instruments"))
        flash("Invalid details!", category="error")
        return redirect(url_for("profile.About"))
    
    if "delete" in request.form:
        db.session.delete(inst)
    else:
        inst.details = request.form.get("details")
        inst.year = request.form.get("year")
        inst.level = request.form.get("level")
    db.session.commit()
    return redirect(url_for("profile.About"))


@profile.route("/HandleSetCountry", methods=["POST"])
@login_required
def HandleSetCountry():
    '''Handles the form submission when the user sets their country'''
    current_user.country = request.form.get("countries")
    db.session.commit()
    return redirect(url_for("profile.About"))


@profile.route("/HandleSetCity", methods=["POST"])
@login_required
def HandleSetCity():
    '''Handles the form submission when the user sets their city'''
    current_user.city = request.form.get("cities")
    db.session.commit()
    return redirect(url_for("profile.About"))


@profile.route("/HandleSetWork", methods=["POST"])
@login_required
def HandleSetWork():
    '''Handles the form submission when the user sets their place of work'''