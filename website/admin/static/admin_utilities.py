from flask import flash, render_template
from flask_login import current_user
from ...models import db, User
from ... import mail
from flask_mail import Message
import datetime


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


def EmailHelpResponse(help, response):
    '''This function emails the response to the user'''
    try:
        # Define email details
        msg = Message("Musician's Haven Query - Response",
            sender = ("Musician's Haven", "musicians.haven.app@gmail.com"),
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