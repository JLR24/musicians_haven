from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from ...models import db, User
from sqlalchemy import or_
from fuzzywuzzy import fuzz

social = Blueprint("social", __name__, template_folder="templates", static_folder="static")


@social.route("/")
@social.route("/find")
@login_required
def Find():
    search = request.args.get("search")
    if search:
        results = search_for_users(search)
    else:
        results = []
    return render_template("find.html", user=current_user, active="Find", search=search, results=results)


@social.route("/profile/<int:id>")
@login_required
def Profile(id):
    if id == current_user.id:
        return redirect(url_for("profile.Current"))
    profile = User.query.filter_by(id=id).first()
    if not profile:
        flash("Invalid details!", category="error")
        return redirect(url_for("social.Find"))
    return f"WIP: {profile.username}"


@social.route("/chats")
@login_required
def Chats():
    return render_template("chats.html", user=current_user, active="Chats")


@social.route("/forums")
@login_required
def Forums():
    return render_template("forums.html", user=current_user, active="Forums")


def search_for_users(search):
    '''Returns a list of user objects whose usernames and names match the given search string.'''

    # To consider: splits (spaces/underscores/dots, etc) in both the search term and the user's username and name. Ratio should be very high (or require a perfect match up until the word length?)
    possible_results = User.query.filter(or_(User.name.like(f"%{search.lower()}%"), User.username.like(f"%{search.lower()}%"))).all() # Source: https://hackersandslackers.com/database-queries-sqlalchemy-orm/
    results = []
    for user in possible_results:
        ratios = []
        username_ratio = fuzz.ratio(user.username.lower()[:len(search)], search.lower())
        if username_ratio > 90:
            ratios.append(username_ratio)
        
        if user.name:
            # Now check against each word in their name.
            for word in user.name.lower().split(" "):
                ratio = fuzz.ratio(word, search.lower())
                if ratio > 90:
                    ratios.append(ratio - 20) # -20 since lots of people will have the same first names
        
        # Now get the maximum ratio and add to the results list
        if len(ratios) > 0:
            results.append((user, max(ratios)))

    return [i[0] for i in sorted(results, key=lambda x: x[1], reverse=True)]