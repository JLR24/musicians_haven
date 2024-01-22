from flask import flash, render_template
from flask_login import current_user
from ...models import User
from ... import mail
from flask_mail import Message
import datetime
from os import getenv


def is_admin():
    '''Returns True if the user is an admin, False (and flashes error) otherwise'''
    if current_user.status != "Admin":
        flash("You don't have permission to view this page.", category="error")
        return False
    return True


def get_editors():
    '''Returns a list of all users with the rank "Editor"'''
    return User.query.filter_by(status="Editor").all()


def get_admins():
    '''Returns a list of all users with the rank "Admin"'''
    return User.query.filter_by(status="Admin").all()


def get_max(input):
    '''Returns the maximum length of lists in the inputted list -> Handles "None"s.'''
    m = 0
    for i in input:
        if i != None and len(i) > m:
            m = len(i)
    return m


def get_banned():
    '''Returns a list of all banned users'''
    return User.query.filter(User.status.startswith("b")).all()


def email_help_response(help, response):
    '''This function emails the response to the user'''
    try:
        # Define email details
        msg = Message("Musician's Haven Query - Response",
            sender = ("Musician's Haven", getenv("EMAIL")),
            recipients = [(help.email)]
        )
        msg.body = f"Response: {response}"
        msg.html = render_template("email_response.html", response=response, help=help, current_date=datetime.datetime.today().strftime('%d/%m/%Y'), user=current_user)
        mail.send(msg)
        return True
    except Exception as e:
        # If the process fails (most likely an account login failure)...
        flash(f'Mail send failure - - "{str(e)}" - - Please try again...', category="error")
        return False
    

def email_missing_response(missing, response):
    '''This function emails the missing report response to the user'''
    try:
        # Define email details
        msg = Message("Musician's Haven Missing Report - Response",
            sender = ("Musician's Haven", getenv("EMAIL")),
            recipients = [(missing.email)]
        )
        msg.body = f"Response: {response}"
        msg.html = render_template("email_missing.html", response=response, missing=missing, current_date=datetime.datetime.today().strftime('%d/%m/%Y'), user=current_user)
        mail.send(msg)
        return True
    except Exception as e:
        # If the process fails (most likely an account login failure)...
        flash(f'Mail send failure - - "{str(e)}" - - Please try again...', category="error")
        return False