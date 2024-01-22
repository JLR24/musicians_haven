from flask import redirect, url_for, flash
from website import create_app, get_notifications

app = create_app()

@app.route("/")
def Home():
    return redirect(url_for("mh.Home"))

@app.errorhandler(404)
def PageNotFound(error):
    flash("That page does not seem to exist! Redirecting to the home page...", category="error")
    return redirect(url_for("mh.Home"))

@app.context_processor
def InjectContent():
    return get_notifications()

if __name__ == "__main__":
    app.run(debug=True)