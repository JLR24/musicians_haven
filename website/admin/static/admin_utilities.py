from flask import flash
from flask_login import current_user
from ...models import db, User


def IsAdmin():
    '''Returns True if the user is an admin, False otherwise'''
    if current_user.status != "Admin":
        flash("You don't have permission to view this page.", category="error")
        return False
    return True


def GetEditors():
    '''Returns a list of all users with the rank "Editor"'''
    return User.query.filter_by(status="Editor").all()


def GetAdmins():
    '''Returns a list of all users with the rank "Admin"'''
    return User.query.filter_by(status="Admin").all()


def GetMax(input):
    '''Returns the maximum length of lists in the inputted list -> Handles "None"s.'''
    m = 0
    for i in input:
        if i != None and len(i) > m:
            m = len(i)
    return m


def GetBanned():
    '''Returns a list of all banned users'''
    return User.query.filter(User.status.startswith("b")).all()