from flask import flash
from flask_login import current_user
from ... import db


def IsAdmin():
    '''Returns True if the user is an admin, False otherwise'''
    if current_user.status != "Admin":
        flash("You don't have permission to view this page.", category="error")
        return False
    return True