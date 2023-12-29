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
    status = db.Column(db.String(1024)) # Admin, User, Editor, Banned (+ reason), Suspended (+ reason)

    def GetPosts(self):
        '''Returns a list of the user's posts ordered by date.'''
        return (sorted(UserPost.query.filter_by(user=self.id).all(), key=lambda i: i.date)).reverse()
    
    def GetFriendLinks(self):
        '''Returns a list of friend links.'''
        return UserLink.query.filter(UserLink.user1==self.id or UserLink.user2==self.id).all()
    
    def GetFriends(self):
        '''Returns a list of the user's friends.'''
        links = sorted(self.GetFriendLinks(), key=lambda i: i.date)
        results = []
        for link in links:
            if link.user1 != self.id:
                results.append(link.user1)
            else:
                results.append(link.user2)
        return results
    
    def GetFeed(self):
        '''Returns the list of posts to appear in the user's feed.'''
        posts = []
        for user in self.GetFriends():
            posts.append(user.GetPosts())
        return sorted(posts, key=lambda i: i.date).reverse()
    
    def FollowsThreads(self):
        '''Returns True if the user follows any threads, False otherwise'''
        if ThreadFollow.query.filter_by(user=self.id).first():
            return True
        return False
    
    def GetFollowedThreadLinks(self):
        '''Returns a list of the user's followed threads'''
        return ThreadFollow.query.filter_by(user=self.id).all()
    
    def GetBanReason(self):
        '''Returns a string containing the reason for the user's ban'''
        return self.status[8:]
    
    def GetInstruments(self):
        '''Returns a list of UserInstrument objects'''
        return UserInstrument.query.filter_by(user=self.id).all()
    
    def GetGenres(self, sort=False):
        '''Returns a list of UserGenre objects, optionally sorted by ranking'''
        if sort:
            return sorted(UserGenre.query.filter_by(user=self.id).all(), key=lambda i: i.ranking)
        return UserGenre.query.filter_by(user=self.id).all()
    
    def GetFavourites(self, sort=False):
        '''Returns a list of UserFavourite objects, optionally sorted by ranking'''
        if sort:
            return sorted(UserFavourite.query.filter_by(user=self.id).all(), key=lambda i: i.ranking)
        return UserFavourite.query.filter_by(user=self.id).all()
    
    def GetNotifications(self, seen=False):
        if seen:
            return Notification.query.filter_by(user=self.id, seen=True).all()
        else:
            return Notification.query.filter_by(user=self.id, seen=False).all()


class UserSetting(db.Model):
    user = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    privacy_policy = db.Column(db.DateTime(timezone=True), default=func.now())
    messaging = db.Column(db.String(32)) # Anyone can message me, People I follow, No one
    account_type = db.Column(db.String(16)) # Public, Private, Hidden (marked for deletion after 28 days)
    notifications = db.Column(db.String(64)) # 1 for yes, 0 for no: { ... }
    '''
    Notification Settings:
     - [0]: Friend request (accept/new)
     - [1]: New content approved
     - [2]: New thread accepted
     - [3]: Thread post reply
     - [4]: Thread post like
     - [5]: Followed thread activity
     - [6]: New message
     - [7]: New chat started
     [ - [8]: Rank change - always on]
    '''
    account_settings = db.Column(db.String(64)) # 1 for yes, 0 for no:
    '''
    Account Settings:
     - [0]: Show name
     - [1]: Show location
     - [2]: Show place of work
     - [3]: Show age (for bands)
    '''


class UserLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey("user.id"))
    user2 = db.Column(db.Integer) # Other user's profile
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String(16)) # Request, Follow, Block, Star
    # Before adding another link between two users, check/update an existing link as required (new block => remove follow (actually update the "status" field))


class UserInstrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    instrument = db.Column(db.String(256))
    details = db.Column(db.String(512))
    year = db.Column(db.Integer)
    level = db.Column(db.String(256))

    @property
    def serialise(self):
        # Source: https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
        return {
            "id": self.id,
            "user": self.user,
            "instrument": self.instrument,
            "details": self.details,
            "year": self.year,
            "level": self.level
        }


class UserGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    genre = db.Column(db.String(256))
    ranking = db.Column(db.Integer) # 0 by default, 1... for ranked.

    @property
    def serialise(self):
        # Source: https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
        return {
            "id": self.id,
            "user": self.user,
            "genre": self.genre,
            "ranking": self.ranking
        }


class UserFavourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    band = db.Column(db.Integer, db.ForeignKey("band.id"))
    ranking = db.Column(db.Integer) # 0 by default, 1-x for top x bands.

    def GetBand(self):
        '''Returns the corresponding Band object'''
        return Band.query.filter_by(id=self.band).first()


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

    def GetGenreString(self):
        '''Returns a string of the band's genres in order of ranking'''
        return sorted(BandGenre.query.filter_by(band=self.id).all(), key=lambda i: i.ranking)


class BandGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    band = db.Column(db.Integer, db.ForeignKey("band.id"))
    genre = db.Column(db.String(256))
    ranking = db.Column(db.Integer)
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
    post_count = db.Column(db.Integer)
    state = db.Column(db.String(16))


class ThreadFollow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread = db.Column(db.Integer, db.ForeignKey("thread.id"))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    last_seen = db.Column(db.Integer)

    def GetThread(self):
        '''Returns the associated thread'''
        return Thread.query.filter_by(id=self.thread).first()
    
    def UserLastSeen(self):
        '''Returns True if the user has seen the last post, False otherwise'''
        if self.last_seen == self.GetThread().post_count:
            return True
        return False


class ThreadPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    thread = db.Column(db.Integer, db.ForeignKey("thread.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.String(16384))
    number = db.Column(db.Integer)
    reply = db.Column(db.Integer, db.ForeignKey("thread_post.id")) # None for not a reply, postID for a reply to that post.
    state = db.Column(db.String(16))


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
    type = db.Column(db.String(32)) # User Search, Song Search, Thread Search, 
    content = db.Column(db.String(8192))
    state = db.Column(db.String(16)) # N/A, Hidden

    def GetUser(self):
        '''Returns the User associated with the Log'''
        return User.query.filter_by(id=self.user).first()


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
    question = db.Column(db.String(8192))


class Missing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320))
    type = db.Column(db.String(128))
    value = db.Column(db.String(256))
    info = db.Column(db.String(2048))


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(128))
    tags = db.Column(db.String(1024))
    content = db.Column(db.String(262144))
    views = db.Column(db.Integer)


# class Playlist(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user = db.Column(db.Integer, db.ForeignKey("user.id"))
#     name = db.Column(db.String(256))
#     date_created = db.Column(db.DateTime(timezone=True), default=func.now())
#     description = db.Column(db.String(2048))
#     public = db.Column(db.Boolean)


# class PlayistCommit(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     playlist = db.Column(db.Integer, db.ForeignKey("playlist.id"))
#     message = db.Column(db.String(256))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())


# class PlaylistChange(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     commit = db.Column(db.Integer, db.ForeignKey("commit.id"))
#     song = db.Column(db.Integer, db.ForeignKey("song.id"))
#     action = db.Column(db.String(64))

# class PlaylistSong(db.Model):
#     pass
#     # is this necessary?