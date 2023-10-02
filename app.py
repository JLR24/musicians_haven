from flask import redirect, url_for, flash, render_template
from website import CreateApp, GetNotifications

app = CreateApp()

@app.route("/")
def Home():
    return redirect(url_for("mh.Home"))

@app.errorhandler(404)
def PageNotFound(error):
    flash("That page does not seem to exist! Redirecting to the home page...", category="error")
    return redirect(url_for("mh.Home"))


@app.context_processor
def InjectContent():
    return GetNotifications()

if __name__ == "__main__":
    app.run(debug=True)
