from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from ...models import db, UserInstrument, UserGenre, Notification
from .static.file_reader import get_instruments, get_cities, get_countries, get_genres
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
    user_instruments = [i.serialise for i in current_user.getInstruments()]
    user_genres = [i.serialise for i in current_user.getGenres()]
    return render_template("profile_settings.html", 
        user=current_user, active="Profile", 
        year=datetime.datetime.now().year, 
        instruments=get_instruments(), 
        user_instruments=user_instruments,
        cities=get_cities(), 
        countries=get_countries(),
        user_genres=user_genres,
        genres = get_genres()
    )


@profile.route("/notifications")
@login_required
def Notifications():
    '''Displays the user's notifications'''
    return render_template("notifications.html", user=current_user, active="Notifications")


@profile.route("/HandleBio", methods=["POST"])
@login_required
def HandleBio():
    '''Handles the form submission when the user sets their bio'''
    bio = request.form.get("bio")
    if len(bio) > 0:
        current_user.bio = bio
    else:
        current_user.bio = None
    db.session.commit()
    return redirect(url_for("profile.About"))


@profile.route("/HandleName", methods=["POST"])
@login_required
def HandleName():
    '''Handles the form submission when the user sets their name'''
    name = request.form.get("name")
    if len(name) > 0:
        current_user.name = name
    else:
        current_user.name = None
    db.session.commit()
    return redirect(url_for("profile.About"))


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
    country = request.form.get("countries")
    if len(country) > 0:
        current_user.country = country
    else:
        current_user.country = None
    db.session.commit()
    return redirect(url_for("profile.About"))


@profile.route("/HandleSetCity", methods=["POST"])
@login_required
def HandleSetCity():
    '''Handles the form submission when the user sets their city'''
    city = request.form.get("cities")
    if len(city) > 0:
        current_user.city = city
    else:
        current_user.city = None
    db.session.commit()
    return redirect(url_for("profile.About"))


@profile.route("/HandleSetWork", methods=["POST"])
@login_required
def HandleSetWork():
    '''Handles the form submission when the user sets their place of work'''
    return "WIP"


@profile.route("/HandleGenres", methods=["POST"])
@login_required
def HandleGenres():
    '''Handles the form submission when the user enters their preferred genres'''
    try:
        length = int(request.form.get("genre_count"))
    except:
        flash("Encountered an unknown error, please try again.", category="error")
        return redirect(url_for("profile.About"))
    
    encounteredGenreIDs = []
    for i in range(length):
        # No way of matching new elements to an ID?
        index = i + 1
        id = request.form.get(f"id:{index}")
        userGenre = UserGenre.query.filter_by(id=id).first()
        if userGenre:
            encounteredGenreIDs.append(userGenre.id)
            userGenre.ranking = request.form.get(f"ranking:{id}")
            db.session.commit()
        else:
            ug = UserGenre(
                user = current_user.id,
                genre = request.form.get(f"genre:{index}"),
                ranking = request.form.get(f"ranking:{index}")
            )
            db.session.add(ug)
            db.session.commit()
            encounteredGenreIDs.append(ug.id)

    ugs = UserGenre.query.filter_by(user=current_user.id).all()
    if len(encounteredGenreIDs) != len(ugs):
        # Some genres have been deleted
        for ug in ugs:
            if ug.id not in encounteredGenreIDs:
                db.session.delete(ug)
    db.session.commit()
    return redirect(url_for("profile.About") + "#genres")


@profile.route("/HandleNotification", methods=["POST"])
@login_required
def HandleNotification():
    '''Handles the form submission when the user reads or clears a notification'''
    notif = Notification.query.filter_by(id=request.form.get("notification"), user=current_user.id).first()
    if not notif:
        flash("Invalid details!", category="error")
        return redirect(url_for("profile.Notifications"))
    if request.form.get("form") == "Unseen": # Mark as seen
        notif.seen = True
    else: # Delete from db
        db.session.delete(notif)
    db.session.commit()
    return redirect(url_for("profile.Notifications"))
