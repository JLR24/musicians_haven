from flask import redirect, url_for, flash
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

# Playlist Tracker:
# - Allows the user to store multiple playlists.
# - Each playlist contains details (name, etc) and songs.
# - Chnges to each playlist are tracked.
# - This means that the user can return to a particular date to find:
#   - Songs added around this time.
#   - The current state of the playlist at this time.
#   - (If there is a change on that day, different times can be viewed).
#   - Research some way of linking this directly to Spotify/Apple?
#   - Also allow for memories (one year ago today...)
    

# FEATURES TO ADD:
# - Consider bandcamp/soundcloud features (owner notes on songs (such as inspiration), links to their other platforms, etc).
# - Playlist tracker.
# - Last Login.
# - Metronome, tempo calculator, chord analyser.