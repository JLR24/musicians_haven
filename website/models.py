from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

### USER ###

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(320))
    password = db.Column(db.String(256))
    icon = db.Column(db.String(4096))
    name = db.Column(db.String(256))
    bio = db.Column(db.String(512))
    dob = db.Column(db.Date)
    country = db.Column(db.String(256))
    city = db.Column(db.String(256))
    place_of_work = db.Column(db.String(512))
    editor_score = db.Column(db.Integer)
    band_status = db.Column(db.String(128)) # Either "Looking", "In a band", "In a band, but may possibly join another", or "Not interested".
    status = db.Column(db.String(1024)) # Admin, User, Banned (+ reason), Suspended (+ reason)


class UserSetting(db.Model):
    user = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    privacy_policy = db.Column(db.DateTime(timezone=True), default=func.now())
    messaging = db.Column(db.String(32)) # Anyone can message me, People I follow, No one
    account_type = db.Column(db.String(16)) # Public, Private, Hidden (marked for deletion after 28 days)
    notifications = db.Column(db.String(64)) # 1 for yes, 0 for no: { ... }


class UserLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey("user.id"))
    user2 = db.Column(db.Integer) # Other user's profile
    status = db.Column(db.String(16)) # Request, Follow, Block, Star
    # Before adding another link between two users, check/update an existing link as required (new block => remove follow (actually update the "status" field))


class UserInstrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    instrument = db.Column(db.String(256))
    details = db.Column(db.String(512))
    year = db.Column(db.Integer)
    level = db.Column(db.String(256))


class UserGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    genre = db.Column(db.String(256))
    ranking = db.Column(db.Integer) # 0 by default, 1... for ranked.


class UserFavourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    band = db.Column(db.Integer, db.ForeignKey("band.id"))
    ranking = db.Column(db.Integer) # 0 by default, 1-x for top x bands.


class UserIdea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(128))
    tags = db.Column(db.String(4096))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    ref_type = db.Column(db.String(128))
    ref = db.Column(db.String(4096))


class UserContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(128))
    type = db.Column(db.String(128)) # Lyrics, guitar tab, chords, etc
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.String(262144))
    details = db.Column(db.String(4096))


class UserPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    filepath = db.Column(db.String(4096))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    caption = db.Column(db.String(4096))
    state = db.Column(db.String(16))


### MESSAGING ###

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    image_filepath = db.Column(db.String(4096))
    date_created = db.Column(db.Date, default=func.now())
    strict_join = db.Column(db.Boolean) # Only "admins" can add members, if all admins leave, the next "oldest" ChatUser is promoted.
    state = db.Column(db.String(16)) # Deleted, hidden (under review)

    def GetRecent(self):
        '''Returns the most recent message from the chat'''
        return "WIP"
    

class ChatUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    chat = db.Column(db.Integer, db.ForeignKey("chat.id"))
    date_joined = db.Column(db.DateTime(timezone=True), default=func.now())
    can_add = db.Column(db.Boolean)

    def GetMessageColour(self):
        '''Returns a (unique-ish) colour for each chat member.'''
        return "WIP"
    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    chat = db.Column(db.Integer, db.ForeignKey("chat.id"))
    state = db.Column(db.String(16)) # Deleted, hidden (under review)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    type = db.Column(db.String(16)) # Message, image, song share, band share
    content = db.Column(db.String(16384))
    
    
class MessageSeen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    message = db.Column(db.Integer, db.ForeignKey("message.id"))
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    # ONLY STORE THE MOST RECENT USER VIEWING FROM EVERY CHAT


### MUSIC ###

class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    date_formed = db.Column(db.Date)
    image_filepath = db.Column(db.String(4096))
    based_in = db.Column(db.String(128)) # City
    state = db.Column(db.String(16))
    owner = db.Column(db.Integer, db.ForeignKey("user.id"))

    def GetListeners(self):
        '''Returns a list of all users that have favourited this band'''


class BandGenres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    band = db.Column(db.Integer, db.ForeignKey("band.id"))
    genre = db.Column(db.String(256))
    state = db.Column(db.String(16))


class BandFact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    band = db.Column(db.Integer, db.ForeignKey("band.id"))
    fact = db.Column(db.String(4096))
    state = db.Column(db.String(16))


class BandMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    band = db.Column(db.Integer, db.ForeignKey("band.id"))
    instrument = db.Column(db.Integer, db.ForeignKey("user_instrument.id"))
    role = db.Column(db.String(2048)) # Producer, mixer, etc...
    date_joined = db.Column(db.Date, default=func.now())
    date_left = db.Column(db.Date)
    state = db.Column(db.String(16))

    def HasLeft(self):
        '''Returns true if this member has left the band'''
        return "WIP"


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    band = db.Column(db.Integer, db.ForeignKey("band.id"))
    date_released = db.Column(db.Date)
    track_number = db.Column(db.Integer)
    image_filepath = db.Column(db.String(4096))
    state = db.Column(db.String(16))


class AlbumFact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album = db.Column(db.Integer, db.ForeignKey("album.id"))
    fact = db.Column(db.String(4096))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    album = db.Column(db.Integer, db.ForeignKey("album.id"))
    isrc = db.Column(db.String(50))
    track_number = db.Column(db.Integer)
    key = db.Column(db.String(100))
    time_sig = db.Column(db.String(50))
    tempo = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    views = db.Column(db.Integer)
    state = db.Column(db.String(50))


class SongFact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song = db.Column(db.Integer, db.ForeignKey("song.id"))
    fact = db.Column(db.String(4096))


class SongContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song = db.Column(db.Integer, db.ForeignKey("song.id"))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    type = db.Column(db.String(128)) # Lyrics, guitar tab, chords, etc
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.String(262144))
    details = db.Column(db.String(4096))
    state = db.Column(db.String(16))


### FORUMS ###

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    creator = db.Column(db.Integer, db.ForeignKey("user.id"))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    info = db.Column(db.String(4096))
    tags = db.Column(db.String(4096))
    state = db.Column(db.String(16))


class ThreadFollow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread = db.Column(db.Integer, db.ForeignKey("thread.id"))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class ThreadPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    thread = db.Column(db.Integer, db.ForeignKey("thread.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.String(16384))
    reply = db.Column(db.Integer, db.ForeignKey("thread_post.id")) # None for not a reply, postID for a reply to that post.


class ThreadPostInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    post = db.Column(db.Integer, db.ForeignKey("thread_post.id"))
    verdict = db.Column(db.String(16)) # Like, Dislike


### OTHER ###

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    type = db.Column(db.String(32))
    content = db.Column(db.String(8192))
    state = db.Column(db.String(16)) # N/A, Hidden


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    type = db.Column(db.String(32)) # Message, reply, request accept, etc...
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.String(8192))
    seen = db.Column(db.Boolean)


class Help(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    query = db.Column(db.String(8192))


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(128))
    tags = db.Column(db.String(1024))
    content = db.Column(db.String(262144))
    views = db.Column(db.Integer)